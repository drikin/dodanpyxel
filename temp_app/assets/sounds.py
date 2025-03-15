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
    
    # BGM - メインメロディー (5) - ユーロビート風
    pyxel.sounds[5] = pyxel.Sound()
    pyxel.sounds[5].set(
        "A3A3A3A3G3G3G3G3F3F3E3E3F3F3G3G3" +  # ユーロビート風メロディ1
        "A3A3A3A3G3G3G3G3C4C4C4C4A3A3G3G3" +  # ユーロビート風メロディ2
        "F3F3F3F3E3E3E3E3D3D3D3D3C3C3D3E3" +  # ユーロビート風メロディ3
        "F3F3F3F3A3A3A3A3C4C4C4C4D4D4E4E4",   # ユーロビート風クライマックス
        "S",  # トーンタイプ: Square wave - よりシャープな音色
        "6",  # ボリューム
        "N",  # エフェクト: None
        12    # スピード - 高速化
    )
    
    # BGM - ベースライン (6) - 16ビートベース
    pyxel.sounds[6] = pyxel.Sound()
    pyxel.sounds[6].set(
        "F2F2F2F2F2F2F2F2C2C2C2C2C2C2C2C2" +  # 16ビートベース1
        "E2E2E2E2E2E2E2E2C2C2C2C2C2C2C2C2" +  # 16ビートベース2
        "D2D2D2D2D2D2D2D2A1A1A1A1A1A1A1A1" +  # 16ビートベース3
        "F2F2F2F2F2F2F2F2G2G2G2G2A2A2A2A2",   # 16ビートベース4
        "T",  # トーンタイプ: Triangle wave
        "5",  # ボリューム
        "N",  # エフェクト: なし - ユーロビートの特徴である持続的なベース
        12    # スピード - 高速化
    )
    
    # BGM - ドラム/パーカッション (7) - 16ビートドラム
    pyxel.sounds[7] = pyxel.Sound()
    pyxel.sounds[7].set(
        "C1RA3C1RA3B3RA3C1RA3C1RA3B3RA3" +  # 16ビートキック、ハイハット、スネアパターン1
        "C1RA3C1RA3B3RA3C1RA3C1RA3B3RA3" +  # 16ビートパターン2
        "C1RA3C1RA3B3RA3C1RA3C1RA3B3RA3" +  # 16ビートパターン3
        "C1RC1RB3RC1RC1RC1RB3RB3RC1RC1R",   # クライマックス16ビート
        "N",  # トーンタイプ: Noise
        "6753",  # ボリューム (各音符ごとに設定)
        "N",  # エフェクト: None - クリアで力強い音
        12    # スピード - 高速化
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
    
    # Sound effect 15: スターウォーズ風のイントロBGM (壮大でゆっくりとした)
    pyxel.sounds[15] = pyxel.Sound()
    pyxel.sounds[15].set(
        "C3E3G3C4" +           # オープニングファンファーレ
        "G3D3G3B3D4" +         # メインテーマの開始
        "F3C3F3A3C4" +         # メインフレーズの続き
        "E3G3B3E4G4" +         # 高揚部分
        "C3G3C4E4G4" +         # 壮大なクライマックス
        "A2C3F3A3C4" +         # エピックな終わり
        "G2B2D3G3B3" +         # フレーズ終わり
        "C3C3G3G3C4C4" +       # ファイナルステートメント
        # 以下、ループ部分を追加して長さを倍増
        "C3E3G3C4" +           # 繰り返し：オープニングファンファーレ
        "G3D3G3B3D4" +         # 繰り返し：メインテーマの開始
        "F3C3F3A3C4" +         # 繰り返し：メインフレーズの続き
        "E3G3B3E4G4" +         # 繰り返し：高揚部分
        "C3G3C4E4G4" +         # 繰り返し：壮大なクライマックス
        "A2C3F3A3C4" +         # 繰り返し：エピックな終わり
        "G2B2D3G3B3" +         # 繰り返し：フレーズ終わり
        "C3C3G3G3C4C4",        # 繰り返し：ファイナルステートメント
        "T",  # トーンタイプ: Triangle wave（より柔らかな音色）
        "4455667744556677",  # ボリューム（徐々に大きく、繰り返し部分も同様）
        "N",  # エフェクト: None (Fade-outをなくして再生時間を延長)
        3     # スピード - より遅くして長く聴こえるように（壮大な感じに）
    )
    
    # Sound effect 16: スターウォーズ風ベース音（低音部）
    pyxel.sounds[16] = pyxel.Sound()
    pyxel.sounds[16].set(
        "C2C2G2G2" +           # 低音での安定感
        "G1G1D2D2" +           # 低い音でのサポート
        "F1F1C2C2" +           # 低音部の変化
        "E1E1B1B1" +           # テンション部分
        "C1C1G1G1" +           # 重厚な低音
        "F1F1C2C2" +           # 低音和音
        "G1G1D2D2" +           # 太い低音
        "C1C1C1C1" +           # 終結部分
        # 以下、ループ部分を追加して長さを倍増
        "C2C2G2G2" +           # 繰り返し：低音での安定感
        "G1G1D2D2" +           # 繰り返し：低い音でのサポート
        "F1F1C2C2" +           # 繰り返し：低音部の変化
        "E1E1B1B1" +           # 繰り返し：テンション部分
        "C1C1G1G1" +           # 繰り返し：重厚な低音
        "F1F1C2C2" +           # 繰り返し：低音和音
        "G1G1D2D2" +           # 繰り返し：太い低音
        "C1C1C1C1",            # 繰り返し：終結部分
        "T",  # トーンタイプ: Triangle wave（よりしっとりとした音色）
        "4444444444444444",  # ボリューム（一定、繰り返し部分も同様）
        "N",  # エフェクト: None
        3     # スピード - 非常にゆっくり（メインBGMと合わせる）
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
