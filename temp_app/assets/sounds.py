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
    
    # BGM - メインメロディー (5) - スタイリッシュなBGM
    pyxel.sounds[5] = pyxel.Sound()
    pyxel.sounds[5].set(
        "A3C4E4A3C4E4G4R" +  # スタイリッシュな導入（クールな印象）
        "G3B3D4G3B3D4F4R" +  # 落ち着いた雰囲気のフレーズ
        "E3G3B3E3G3B3D4R" +  # 深みのあるメロディライン
        "A3C4E4A3C4E4A4R" +  # 上昇感のある洗練されたフレーズ
        
        # 拡張パート（より洗練された印象）
        "G3B3D4F4G3B3D4F4" +  # クールな進行
        "E3G3B3D4E3G3B3D4" +  # 落ち着きある展開
        "A3C4E4G4A3C4E4G4" +  # 深みと広がりを感じるフレーズ
        "F3A3C4E4F3A3C4E4" +  # スタイリッシュな変化
        
        # クライマックスパート
        "E3G3B3D4E3G3B3D4" +  # 深みのあるクライマックス
        "A3C4E4G4A3C4E4G4" +  # 力強さと洗練さを兼ね備えたフレーズ
        "G3B3D4F4G3B3D4F4" +  # 緊張感と期待感を高めるライン
        "E3G3B3D4E3G3B3D4" +  # スタイリッシュな終結へ
        
        # フィナーレ
        "A3C4E4A4A3C4E4A4" +  # 洗練された仕上げ
        "G3B3D4G4G3B3D4G4" +  # 深みを保ちながら収束へ
        "E3G3B3E4E3G3B3E4" +  # クールな印象を残す終わり方
        "A3E4A4C4E4A4E4R",    # スタイリッシュな締めくくり
        
        "T",  # トーンタイプ: Triangle wave - より滑らかでスタイリッシュな音色
        "4444444444444444", # ボリューム（均一で落ち着いた音量）
        "N",  # エフェクト: None - クリーンでシャープな印象
        14    # スピード - やや落ち着いたテンポでスタイリッシュに
    )
    
    # BGM - ベースライン (6) - スタイリッシュで重厚感のあるベースライン
    pyxel.sounds[6] = pyxel.Sound()
    pyxel.sounds[6].set(
        "A1E1A1E1A1E1A1E1" +  # 落ち着いたベースライン（スタイリッシュな印象）
        "G1D1G1D1G1D1G1D1" +  # メロディに合わせた低音部
        "E1B1E1B1E1B1E1B1" +  # 深みのある音で安定感
        "A1E1A1E1A1E1A1E1" +  # 反復で統一感を出す
        
        # 拡張パート（メロディに合わせて）
        "G1D1G1D1G1D1G1D1" +  # スタイリッシュな低音
        "E1B1E1B1E1B1E1B1" +  # 落ち着いた雰囲気を支える
        "A1E1A1E1A1E1A1E1" +  # 安定したベースライン
        "F1C1F1C1F1C1F1C1" +  # 変化を付けつつ統一感を維持
        
        # クライマックスパート
        "E1B1E1B1E1B1E1B1" +  # 低音で重厚感を出す
        "A1E1A1E1A1E1A1E1" +  # スタイリッシュな進行
        "G1D1G1D1G1D1G1D1" +  # 安定感のある低音
        "E1B1E1B1E1B1E1B1" +  # クールな印象を維持
        
        # フィナーレ
        "A1E1A1E1A1E1A1E1" +  # 統一感あるベースライン
        "G1D1G1D1G1D1G1D1" +  # 落ち着いた雰囲気で収束へ
        "E1B1E1B1E1B1E1B1" +  # スタイリッシュに終わりへ
        "A1E1A1E1A1E1A1E1",   # 一貫性のある締めくくり
        
        "S",  # トーンタイプ: Square wave - シャープな低音
        "3333333333333333",  # ボリューム（控えめで一定）
        "N",  # エフェクト: なし - クリーンな音質
        14    # スピード - メインメロディと合わせてやや落ち着いたテンポ
    )
    
    # BGM - ドラム/パーカッション (7) - スタイリッシュな4ビートドラム
    pyxel.sounds[7] = pyxel.Sound()
    pyxel.sounds[7].set(
        "C1RA2RC1RA2RR" +  # 洗練された4ビートパターン（高音ハイハットを控えめに）
        "C1RA2RC1RA2RR" +  # リピート（安定感）
        "C1RA2RC1RA2RR" +  # リピート（一貫性）
        "C1RA2RC1RB2RR" +  # 微妙な変化（スネアを控えめに）
        
        # 拡張パート - より落ち着いたドラムパターン
        "C1RA2RRRA2RC1" +  # スタイリッシュなパターン（余白を持たせる）
        "RC1RA2RC1RA2R" +  # リズムの変化（キック位置変更）
        "C1RRC1RA2RRA2" +  # シンプルに洗練された印象
        "RC1RA2RRC1RA2" +  # 変化しつつ統一感
        
        # 深みのあるパート
        "C1RRC1RRA2RR" +  # スペースを活かした構成
        "A2RRC1RRA2RR" +  # ミニマルな印象
        "C1RA2RRC1RA2R" +  # 洗練された展開
        "RRC1RA2RC1RR" +  # スタイリッシュなフィル
        
        # フィナーレ
        "C1RA2RC1RA2RR" +  # 基本に戻る（統一感）
        "C1RA2RC1RA2RR" +  # 一貫性を維持
        "C1RRC1RRA2RR" +  # よりミニマルに
        "C1RC1RA2RRRR",    # 余韻を残す終わり方
        
        "N",  # トーンタイプ: Noise
        "3333333333333333",  # ボリューム (控えめで耳障りにならない強さ)
        "F",  # エフェクト: Fade out - より洗練された印象に
        14    # スピード - メインメロディとベースに合わせる
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
    
    # Sound effect 15: スターウォーズ風のイントロBGM (非常に壮大でワクワクさせる)
    pyxel.sounds[15] = pyxel.Sound()
    pyxel.sounds[15].set(
        "C2E2G2C3" +      # オープニングファンファーレ（より壮大に）
        "G2D2G2B2D3" +   # メインテーマの開始（低音から、ゆったりと）
        "F2C2F2A2C3" +   # メインフレーズの続き（ゆっくりと雄大に）
        "E2G2B2E3G3" +   # 高揚部分（徐々に盛り上がる）
        "C2G2C3E3G3" +   # 壮大なクライマックス（ゆったり）
        "A1C2F2A2C3" +   # エピックな終わり（低音から始まる）
        "G1B1D2G2B2" +   # フレーズ終わり（壮大に）
        "C2G2C3G3G3",    # ファイナルステートメント（印象的に）
        "T",  # トーンタイプ: Triangle wave（より柔らかく雄大に）
        "3333333333333333333333333333333333333333",  # ボリューム（控えめに）
        "N",  # エフェクト: None
        0     # スピード - 最もゆっくり（非常に壮大な宇宙感、より強調）
    )
    
    # Sound effect 16: スターウォーズ風ベース音（重厚な低音部）
    pyxel.sounds[16] = pyxel.Sound()
    pyxel.sounds[16].set(
        "C0G0" +       # より低音での始まり（シンプルに）
        "F0C1" +       # さらに低い音（宇宙の広がりを表現）
        "G0D1" +       # 低音での盛り上がり（壮大さを演出）
        "C1G1" +       # 再び基本音へ（ゆったりと）
        "A0E1" +       # 変化音（雄大な広がり）
        "F0C1" +       # 再び低音へ（壮大な宇宙感）
        "G0G0" +       # 持続低音（緊張感を演出）
        "C1C1",        # 最終和音（長く重厚に）
        "P",  # トーンタイプ: Pulse wave（より深い響きに）
        "4444444444444444",  # ボリューム（音符数に合わせて）
        "N",  # エフェクト: None（持続的な低音の響き）
        0     # スピード - 最もゆっくり（メインメロディと合わせて壮大さを強調）
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
