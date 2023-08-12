import thinkgear
import datetime

def main():
    # 出力するCSVファイルのパスを指定
    file_path = "brain_wave_data.csv"

    # フラグを初期化（このフラグは信号品質が良好かどうかを示す）
    wflag = False

    # データを保存するバッファを初期化
    data_buffer = {}

    # CSVファイルを書き込みモードで開く
    with open(file_path, mode="w") as f:
        # CSVファイルのヘッダー行を書き込む
        f.write("datetime, raw_wave, delta, theta, lowalpha, highalpha, lowbeta, highbeta, lowgamma, midgamma, attention, meditation\n")

        # MindWaveからデータパケットを取得
        for pkt in thinkgear.ThinkGearProtocol('COM4').get_packets():
            # データパケット内の各データを処理
            for d in pkt:
                # 信号品質データの場合
                if isinstance(d, thinkgear.ThinkGearPoorSignalData):
                    # 信号品質が良好（値が10未満）であればフラグを立てる
                    if d.value < 10:
                        wflag = True
                    else:
                        wflag = False

                # 生の脳波データの場合
                if wflag and isinstance(d, thinkgear.ThinkGearRawWaveData):
                    # バッファに生の脳波データを保存
                    data_buffer["raw_wave"] = d.value

                # EEGパワーデータの場合
                if wflag and isinstance(d, thinkgear.ThinkGearEEGPowerData):
                    # バッファに各波長のパワーデータを保存
                    data_buffer["delta"] = d.value.delta
                    data_buffer["theta"] = d.value.theta
                    data_buffer["lowalpha"] = d.value.lowalpha
                    data_buffer["highalpha"] = d.value.highalpha
                    data_buffer["lowbeta"] = d.value.lowbeta
                    data_buffer["highbeta"] = d.value.highbeta
                    data_buffer["lowgamma"] = d.value.lowgamma
                    data_buffer["midgamma"] = d.value.midgamma

                # Attentionデータの場合
                if wflag and isinstance(d, thinkgear.ThinkGearAttentionData):
                    # バッファにAttentionデータを保存
                    data_buffer["attention"] = d.value

                # Meditationデータの場合
                if wflag and isinstance(d, thinkgear.ThinkGearMeditationData):
                    # バッファにMeditationデータを保存
                    data_buffer["meditation"] = d.value

            # バッファにすべてのデータが揃ったらCSVファイルに出力
            if "raw_wave" in data_buffer and "delta" in data_buffer and "attention" in data_buffer and "meditation" in data_buffer:
                # CSVファイルに出力
                f.write("{},{},{},{},{},{},{},{},{},{},{},{}\n".format(datetime.datetime.now(), data_buffer["raw_wave"], data_buffer["delta"], data_buffer["theta"], data_buffer["lowalpha"], data_buffer["highalpha"], data_buffer["lowbeta"], data_buffer["highbeta"], data_buffer["lowgamma"], data_buffer["midgamma"], data_buffer["attention"], data_buffer["meditation"]))
                # コンソールに出力
                print("datetime: {}, raw_wave: {}, delta: {}, theta: {}, lowalpha: {}, highalpha: {}, lowbeta: {}, highbeta: {}, lowgamma: {}, midgamma: {}, attention: {}, meditation: {}".format(datetime.datetime.now(), data_buffer["raw_wave"], data_buffer["delta"], data_buffer["theta"], data_buffer["lowalpha"], data_buffer["highalpha"], data_buffer["lowbeta"], data_buffer["highbeta"], data_buffer["lowgamma"], data_buffer["midgamma"], data_buffer["attention"], data_buffer["meditation"]))
                # バッファをクリア
                data_buffer.clear()

if __name__ == '__main__':
    main()