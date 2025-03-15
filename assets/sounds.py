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
    
    # 通常BGMの設定
    pyxel.musics[0] = pyxel.Music()
    pyxel.musics[0].set([5], [6], [7], [])
    
    # ボス戦BGMの設定
    pyxel.musics[1] = pyxel.Music()
    pyxel.musics[1].set([8], [9], [10], [])
