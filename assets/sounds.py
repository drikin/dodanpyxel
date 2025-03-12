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
    
    # BGM - メインメロディー (5)
    pyxel.sounds[5] = pyxel.Sound()
    pyxel.sounds[5].set(
        "F3F3F3F3G3G3A3A3C4C4A3A3G3G3F3F3" +  # メインフレーズ1
        "E3E3E3E3F3F3G3G3A3A3G3G3F3F3E3E3" +  # メインフレーズ2
        "D3D3D3D3E3E3F3F3G3G3F3F3E3E3D3D3" +  # メインフレーズ3
        "F3F3G3G3A3A3C4C4D4D4C4C4A3A3G3G3",   # クライマックス
        "T",  # トーンタイプ: Triangle wave
        "6",  # ボリューム
        "N",  # エフェクト: None
        25    # スピード - 数値が大きいほど遅く
    )
    
    # BGM - ベースライン (6)
    pyxel.sounds[6] = pyxel.Sound()
    pyxel.sounds[6].set(
        "F2RF2C2RC2F2RF2C2RC2" +  # ベースライン1: -を休符Rに置き換え
        "E2RE2C2RC2E2RE2C2RC2" +  # ベースライン2: -を休符Rに置き換え
        "D2RD2A1RA1D2RD2A1RA1" +  # ベースライン3: -を休符Rに置き換え
        "F2RF2C2RC2F2RF2G2RG2",   # ベースライン4: -を休符Rに置き換え
        "S",  # トーンタイプ: Square wave
        "5",  # ボリューム
        "F",  # エフェクト: Fade out
        25    # スピード
    )
    
    # BGM - ドラム/パーカッション (7)
    pyxel.sounds[7] = pyxel.Sound()
    pyxel.sounds[7].set(
        "C1RRC1RRC1RRC1RR" +   # キック
        "RRRA3RRRA3RRRA3RRRA3" +   # ハイハット（'H'→'A3'に置き換え）
        "RRRRB3RRRRRRB3RRRR" +   # スネア（'S'→'B3'に置き換え）
        "C1RRC1RRC1B3RRC1RR",    # キック+スネア（'S'→'B3'に置き換え）
        "N",  # トーンタイプ: Noise
        "6743",  # ボリューム (各音符ごとに設定)
        "F",  # エフェクト: Fade out
        20    # スピード - リズムセクション
    )
    
    # ボス戦BGM - メインメロディー (8)
    pyxel.sounds[8] = pyxel.Sound()
    pyxel.sounds[8].set(
        "C3RC3RC3RD3RD3RD3RE3RE3RF3RF3RE3RD3R" + # 緊張感のあるメロディ1
        "C3RC3RC3RD3RD3RD3RF3RF3RG3RG3RF3RE3R" + # 緊張感のあるメロディ2
        "E3RE3RE3RF3RF3RF3RG3RG3RA3RA3RG3RF3R" + # 上昇するメロディ
        "C4RC4RB3RB3RA3RA3RG3RG3RF3RF3RE3RD3R",  # 緊張の頂点 (C5→C4に変更)
        "P",  # トーンタイプ: Pulse wave
        "7",  # ボリューム
        "N",  # エフェクト: None
        15    # スピード - 数値が小さいほど速い
    )
    
    # ボス戦BGM - ベース (9)
    pyxel.sounds[9] = pyxel.Sound()
    pyxel.sounds[9].set(
        "C2RRG2RRC2RRG2RR" +  # 重いベースライン1
        "B1RRF2RRB1RRF2RR" +  # 重いベースライン2
        "A1RRE2RRA1RRE2RR" +  # 重いベースライン3
        "F1RRC2RRF1RRG1RR",   # 重いベースライン4
        "T",  # トーンタイプ: Triangle wave
        "5",  # ボリューム
        "F",  # エフェクト: Fade out
        15    # スピード
    )
    
    # ボス戦BGM - リズム (10)
    pyxel.sounds[10] = pyxel.Sound()
    pyxel.sounds[10].set(
        "C1RA3RB3RA3RC1RA3RB3RA3R" +  # キック-ハイハット-スネア-ハイハット
        "C1RA3RB3RA3RC1RA3RB3RA3R" +  # 繰り返し
        "C1RA3RB3RA3RC1RA3RB3RA3R" +  # 繰り返し
        "C1RC1RB3RB3RC1RC1RB3RB3R",  # クライマックス (H→A3, S→B3に置き換え)
        "N",  # トーンタイプ: Noise
        "7775",  # ボリューム (各音符ごとに設定)
        "N",  # エフェクト: None
        15    # スピード - リズムセクション (速い)
    )
    
    # 通常BGMの設定
    pyxel.musics[0] = pyxel.Music()
    pyxel.musics[0].set([5], [6], [7], [])
    
    # ボス戦BGMの設定
    pyxel.musics[1] = pyxel.Music()
    pyxel.musics[1].set([8], [9], [10], [])
