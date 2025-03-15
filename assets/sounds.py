import pyxel
from constants import *

def init_sounds():
    """Initialize game sound effects and music"""
    
    # Sound effect 0: Player shot
    pyxel.sounds[0] = pyxel.Sound()
    pyxel.sounds[0].set("C3C4", "T", "7", "N", 20)
    
    # Sound effect 1: Explosion
    pyxel.sounds[1] = pyxel.Sound()
    pyxel.sounds[1].set("F2F1", "N", "7", "F", 10)
    
    # Sound effect 2: Game Start
    pyxel.sounds[2] = pyxel.Sound()
    pyxel.sounds[2].set("C3E3G3C4", "T", "7", "N", 10)
    
    # Sound effect 3: Game Over
    pyxel.sounds[3] = pyxel.Sound()
    pyxel.sounds[3].set("C4G3E3C3", "S", "7", "F", 5)

    # Sound effect 4: PowerUp
    pyxel.sounds[4] = pyxel.Sound()
    pyxel.sounds[4].set("C3E3G3C4E4G4", "T", "7", "S", 10)
    
    # Sound effect 20: ボス警告音 (アラーム風サイレン)
    pyxel.sounds[20] = pyxel.Sound()
    pyxel.sounds[20].set("C4F4C4F4", "S", "7", "F", 8)
    
    # Sound effect 21: ボス出現音 (ドラマチック)
    pyxel.sounds[21] = pyxel.Sound()
    pyxel.sounds[21].set("C3G3C4E4G4B4", "T", "7", "F", 6)
    
    # Sound effect 11: キーボード入力音
    pyxel.sounds[11] = pyxel.Sound()
    pyxel.sounds[11].set("C4", "P", "4", "N", 30) # 短く軽い音
    
    # Sound effect 12: 確定ボタン音
    pyxel.sounds[12] = pyxel.Sound()
    pyxel.sounds[12].set("C4E4G4", "T", "5", "N", 20) # 確定音
    
    # ここからBGMパート
    
    # BGM - メインメロディー (5) - テンポの良いユーロビート風（拡張版）
    pyxel.sounds[5] = pyxel.Sound()
    pyxel.sounds[5].set(
        "A3A3A3A3G3G3G3G3F3F3E3E3F3F3G3G3" +  # ユーロビート風メロディ1
        "A3A3A3A3G3G3G3G3C4C4C4C4A3A3G3G3" +  # ユーロビート風メロディ2
        "F3F3F3F3E3E3E3E3D3D3D3D3C3C3D3E3" +  # ユーロビート風メロディ3
        "F3F3F3F3A3A3A3A3C4C4C4C4D4D4E4E4" +   # ユーロビート風クライマックス
        # 以下、拡張パート（より長く、変化に富んだシーケンス）
        "C4C4C4C4A3A3A3A3F3F3F3F3D3D3D3D3" +  # 高音パート（エネルギッシュ）
        "E4E4E4E4C4C4C4C4A3A3A3A3F3F3F3F3" +  # 高音からの下降（躍動感）
        "G3G3G3G3A3A3A3A3C4C4C4C4E4E4E4E4" +  # 再上昇（ドライブ感）
        "D4D4D4D4F4F4F4F4E4E4E4E4C4C4C4C4" +  # 高音変化（ダイナミック）
        "A3A3A3A3B3B3B3B3C4C4C4C4D4D4D4D4" +  # さらなる上昇（盛り上がり）
        "E4E4E4E4G4G4G4G4F4F4F4F4D4D4D4D4" +  # クライマックス（最高潮）
        "C4C4C4C4A3A3A3A3E3E3E3E3G3G3G3G3" +  # 下降パート（締めくくり）
        "A3A3A3A3C4C4C4C4A3A3A3A3F3F3F3F3",   # フィナーレ（勢いを維持）
        "S",  # トーンタイプ: Square wave - シャープでエネルギッシュな音色
        "66666666",  # ボリューム（一定で力強く）
        "N",  # エフェクト: None（クリアで持続的な音）
        13    # スピード - さらに高速化（よりテンポ良く）
    )
    
    # BGM - ベースライン (6) - 16ビートベース（拡張版）
    pyxel.sounds[6] = pyxel.Sound()
    pyxel.sounds[6].set(
        "F2F2F2F2F2F2F2F2C2C2C2C2C2C2C2C2" +  # 16ビートベース1
        "E2E2E2E2E2E2E2E2C2C2C2C2C2C2C2C2" +  # 16ビートベース2
        "D2D2D2D2D2D2D2D2A1A1A1A1A1A1A1A1" +  # 16ビートベース3
        "F2F2F2F2F2F2F2F2G2G2G2G2A2A2A2A2" +  # 16ビートベース4
        # 追加パート（メインメロディーの拡張に合わせて）
        "C2C2C2C2C2C2C2C2F2F2F2F2F2F2F2F2" +  # 拡張ベース1（強い推進力）
        "A1A1A1A1A1A1A1A1D2D2D2D2D2D2D2D2" +  # 拡張ベース2（低音でサポート）
        "G1G1G1G1G1G1G1G1C2C2C2C2E2E2E2E2" +  # 拡張ベース3（上昇感）
        "D2D2D2D2D2D2D2D2F2F2F2F2F2F2F2F2" +  # 拡張ベース4（変化）
        "E2E2E2E2E2E2E2E2G2G2G2G2G2G2G2G2" +  # 拡張ベース5（さらなる上昇）
        "A2A2A2A2A2A2A2A2F2F2F2F2D2D2D2D2" +  # 拡張ベース6（クライマックス）
        "C2C2C2C2C2C2C2C2E2E2E2E2E2E2E2E2" +  # 拡張ベース7（下降）
        "F2F2F2F2F2F2F2F2F2F2F2F2F2F2F2F2",   # 拡張ベース8（締め）
        "T",  # トーンタイプ: Triangle wave（適切な厚みの音）
        "55555555",  # ボリューム（安定した力強さ）
        "N",  # エフェクト: なし - ユーロビートの特徴である持続的なベース
        13    # スピード - メインメロディーに合わせて高速化
    )
    
    # BGM - ドラム/パーカッション (7) - 16ビートドラム（拡張版）
    pyxel.sounds[7] = pyxel.Sound()
    pyxel.sounds[7].set(
        "C1RA3C1RA3B3RA3C1RA3C1RA3B3RA3" +  # 16ビートキック、ハイハット、スネアパターン1
        "C1RA3C1RA3B3RA3C1RA3C1RA3B3RA3" +  # 16ビートパターン2
        "C1RA3C1RA3B3RA3C1RA3C1RA3B3RA3" +  # 16ビートパターン3
        "C1RC1RB3RC1RC1RC1RB3RB3RC1RC1R" +  # クライマックス16ビート
        # 以下、拡張パート
        "C1RA3C1RA3B3RA3C1RA3C1RA3B3RA3" +  # 拡張リズム1（基本パターン）
        "C1RB3C1RB3C1RB3C1RC1RB3C1RB3C1" +  # 拡張リズム2（より複雑なパターン）
        "C1RA3C1RA3B3RA3C1RC1RA3B3RA3B3" +  # 拡張リズム3（変化型）
        "C1RB3C1RB3C1RC1RB3RC1RB3C1RC1R" +  # 拡張リズム4（複雑な変化）
        "C1RA3B3RA3C1RA3B3RA3C1RA3B3RA3" +  # 拡張リズム5（基本に戻る）
        "C1RC1RB3RC1RC1RC1RB3RB3RC1RC1R" +  # 拡張リズム6（クライマックス再現）
        "C1RC1RB3RC1RA3RC1RB3RC1RA3RC1R" +  # 拡張リズム7（フィルイン）
        "C1RB3RA3RB3RA3RC1RB3RC1RC1RC1R",   # 拡張リズム8（終結部）
        "N",  # トーンタイプ: Noise
        "67536753675367536753675367536753",  # ボリューム (各音符ごとに設定、要素ごとに調整)
        "N",  # エフェクト: None - クリアで力強い音を維持
        13    # スピード - メインメロディーとベースに合わせて高速化
    )
    
    # ボス戦BGM - メインメロディー (8) - 16ビートユーロビート風
    pyxel.sounds[8] = pyxel.Sound()
    pyxel.sounds[8].set(
        "C4C4C4C4A3A3A3A3F3F3F3F3G3G3G3G3" + # 16ビートユーロビート風メロディ1
        "D4D4D4D4B3B3B3B3G3G3G3G3A3A3A3A3" + # 16ビートユーロビート風メロディ2
        "E4E4E4E4C4C4C4C4A3A3A3A3B3B3B3B3" + # 16ビートユーロビート風メロディ3
        "F4F4F4F4E4E4E4E4D4D4D4D4C4C4C4C4",  # 16ビートユーロビート風クライマックス
        "S",  # トーンタイプ: Square wave - より電子的
        "7",  # ボリューム
        "N",  # エフェクト: None
        10    # スピード - さらに高速化
    )
    
    # ボス戦BGM - ベース (9) - 16ビートユーロビート風
    pyxel.sounds[9] = pyxel.Sound()
    pyxel.sounds[9].set(
        "C2C2C2C2G2G2G2G2C2C2C2C2G2G2G2G2" +  # 16ビートボスベース1
        "B1B1B1B1F2F2F2F2B1B1B1B1F2F2F2F2" +  # 16ビートボスベース2
        "A1A1A1A1E2E2E2E2A1A1A1A1E2E2E2E2" +  # 16ビートボスベース3
        "F1F1F1F1C2C2C2C2F1F1F1F1G1G1G1G1",   # 16ビートボスベース4
        "T",  # トーンタイプ: Triangle wave
        "6",  # ボリューム - 少し大きく
        "N",  # エフェクト: None - 持続的なベース
        10    # スピード - さらに高速化
    )
    
    # ボス戦BGM - リズム (10) - 16ビートユーロビート風
    pyxel.sounds[10] = pyxel.Sound()
    pyxel.sounds[10].set(
        "C1A3B3A3C1A3B3A3C1A3B3A3C1A3B3A3" +  # 16ビートドラムパターン1
        "C1A3B3A3C1A3B3A3C1A3B3A3C1A3B3A3" +  # 16ビートドラムパターン2
        "C1A3C1A3B3A3B3A3C1A3C1A3B3A3B3A3" +  # 16ビートドラムパターン3変化形
        "C1C1B3B3C1C1B3B3C1C1B3B3C1C1C1C1",   # 16ビートクライマックス
        "N",  # トーンタイプ: Noise
        "7664",  # ボリューム (各音符ごとに設定)
        "N",  # エフェクト: None
        10    # スピード - さらに高速化
    )
    
    # Sound effect 15: スターウォーズ風のイントロBGM (非常に壮大でゆったりとした)
    pyxel.sounds[15] = pyxel.Sound()
    pyxel.sounds[15].set(
        "C3E3G3C4" +      # オープニングファンファーレ（シンプルに）
        "G3D3G3B3D4" +    # メインテーマの開始（音数を減らして処理しやすく）
        "F3C3F3A3C4" +    # メインフレーズの続き（ゆっくりと雄大に）
        "E3G3B3E4G4" +    # 高揚部分（シンプルに）
        "C3G3C4E4G4" +    # 壮大なクライマックス（ゆったり）
        "A2C3F3A3C4" +    # エピックな終わり（シンプルに）
        "G2B2D3G3B3" +    # フレーズ終わり（壮大に）
        "C3G3C4G4G4" +    # ファイナルステートメント（C5を避けてG4に変更）
        # 追加部分でより壮大な感じに
        "F2C3F3A3C4" +    # 新しい壮大なフレーズ1
        "G2D3G3B3D4" +    # 新しい壮大なフレーズ2
        "A2E3A3C4E4" +    # 新しい壮大なフレーズ3
        "C3G3E4G4G4",     # 最終的なクライマックス（C5をG4に変更）
        "T",  # トーンタイプ: Triangle wave（より柔らかく雄大に）
        "3333333333333333333333333333333333333333333333333333333333",  # ボリューム（控えめに）
        "N",  # エフェクト: None
        1     # スピード - 超ゆっくり（非常に壮大な宇宙感）
    )
    
    # Sound effect 16: スターウォーズ風ベース音（重厚な低音部）
    pyxel.sounds[16] = pyxel.Sound()
    pyxel.sounds[16].set(
        "C1G1" +       # より低音での始まり（シンプルに）
        "F0C1" +       # さらに低い音（宇宙の広がりを表現）
        "G0D1" +       # 低音での盛り上がり（壮大さを演出）
        "C1G1" +       # 再び基本音へ（ゆったりと）
        "A0E1" +       # 変化音（雄大な広がり）
        "F0C1" +       # 再び低音へ（壮大な宇宙感）
        "G0G0" +       # 持続低音（緊張感を演出）
        "C1C1" +       # 最終和音（長く重厚に）
        # 拡張部分（より豊かな表現）
        "C1G1" +       # 基本音の繰り返し（ゆったり）
        "F0C1" +       # 低音の繰り返し（重厚に）
        "G0D1" +       # 低音変化の繰り返し（壮大に）
        "C0C0",        # 最低音での終結（非常に重厚に）
        "S",  # トーンタイプ: Square wave（よりパワフルに）
        "444444444444444444444444",  # ボリューム（音符数に合わせて）
        "N",  # エフェクト: None（持続的な低音の響き）
        1     # スピード - 超ゆっくり（メインメロディと合わせて非常に壮大に）
    )
    
    # 通常BGMの設定
    pyxel.musics[0] = pyxel.Music()
    pyxel.musics[0].set([5], [6], [7], [])
    
    # ボス戦BGMの設定
    pyxel.musics[1] = pyxel.Music()
    pyxel.musics[1].set([8], [9], [10], [])
    
    # イントロBGMの設定
    pyxel.musics[2] = pyxel.Music()
    pyxel.musics[2].set([15], [16], [], [])
