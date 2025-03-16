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
    
    # BGM - メインメロディー (5) - 爽やかでポップな新BGM
    pyxel.sounds[5] = pyxel.Sound()
    pyxel.sounds[5].set(
        "E4E4G4G4E4G4A4R" +  # 明るく爽やかな導入パート
        "C4C4B4B4A4A4G4R" +  # 高音で爽快感を表現
        "A4A4G4G4F4F4E4R" +  # 下降するメロディライン
        "E4G4A4B4C4D4E4R" +  # 上昇する爽快感あるフレーズ
        
        # 拡張パート（より明るく華やかなメロディ）
        "G4G4E4E4C4C4E4G4" +  # 軽快な上下メロディ
        "A4A4G4G4E4E4G4A4" +  # 躍動感のある進行
        "C4C4A4A4G4G4A4C4" +  # 高音パートで開放感を演出
        "D4D4C4C4A4A4G4G4" +  # メロディの展開
        
        # クライマックスパート
        "E4E4D4D4C4C4B4B4" +  # 高音で明るく弾むような感じ
        "A4A4G4G4F4F4E4E4" +  # 下降しながらも躍動感を維持
        "G4A4B4C4D4E4D4C4" +  # 上昇→下降のダイナミックなライン
        "B4A4G4E4C4G4E4C4" +  # 華やかなアルペジオ風フレーズ
        
        # フィナーレ
        "C4E4G4E4C4G4E4C4" +  # 広がりのある明るいフレーズ
        "A4C4E4C4A4E4C4A3" +  # 下降しながらも爽やかさを維持
        "G4B4D4B4G4D4B3G3" +  # 明るさを保ちながら収束
        "C4E4G4C4E4G4C4R",    # 上昇して締めくくる華やかなエンディング
        
        "P",  # トーンタイプ: Pulse wave - より明るく爽やかな音色
        "6666666677777777", # ボリューム（パートごとに調整、後半を強めに）
        "F",  # エフェクト: Fade out - より洗練された印象に
        16    # スピード - 軽快なテンポ
    )
    
    # BGM - ベースライン (6) - 爽やかで躍動感あるベースライン
    pyxel.sounds[6] = pyxel.Sound()
    pyxel.sounds[6].set(
        "C2G1C2E2C2G1C2E2" +  # 導入部の軽快なベースライン
        "A1E1A1C2A1E1A1C2" +  # 高音メロディに合わせたベース
        "F1C2F1A1F1C2F1A1" +  # 下降メロディをサポート
        "C2G1C2E2G2E2C2G1" +  # 上昇フレーズに合わせた躍動感
        
        # 拡張パート（メロディに合わせて）
        "C2RC2E2C2RC2E2" +  # 軽快な弾むリズム（RはRestで休符）
        "A1RA1C2A1RA1C2" +  # スキップするような躍動感
        "F1RF1A1F1RF1A1" +  # 弾むベースライン
        "G1RG1B1G1RG1D2" +  # 変化をつけた躍動感
        
        # クライマックスに合わせた強化パート
        "C2C2G1G1C2C2E2E2" +  # より強いビートで盛り上げる
        "A1A1E1E1A1A1C2C2" +  # リズミカルな展開
        "G1G1D2D2G1G1B1B1" +  # リズムを強調
        "C2E2G2C3G2E2C2G1" +  # アルペジオ風の上下動
        
        # フィナーレ
        "C2G1C2E2G2E2C2G1" +  # 広がりのあるベースライン
        "A1E1A1C2E2C2A1E1" +  # メロディに寄り添うライン
        "G1D1G1B1D2B1G1D1" +  # 躍動感ある下降
        "C1G1C2E2G2C3G2E2",   # 壮大な締めくくり
        
        "S",  # トーンタイプ: Square wave - より明確なベース音に
        "4444444444444444",  # ボリューム（後半盛り上げ）
        "N",  # エフェクト: なし - 安定した躍動感
        16    # スピード - メインメロディに合わせて軽快に
    )
    
    # BGM - ドラム/パーカッション (7) - 爽やかな8ビートドラム
    pyxel.sounds[7] = pyxel.Sound()
    pyxel.sounds[7].set(
        "C1RA3RC1RA3B3R" +  # 軽快な8ビートパターン1
        "C1RA3RC1RA3B3R" +  # リピート
        "C1RA3RC1RA3B3R" +  # リピート
        "C1RA3RB3RA3C1R" +  # バリエーション
        
        # 拡張パート - より爽やかで軽快なドラムパターン
        "C1RA3RA3RB3RC1" +  # 軽快なパターン（ハイハット強調）
        "RC1RA3RC1RB3RA3" +  # リズムの変化（キック位置変更）
        "RC1RC1RA3RB3RA3" +  # より弾むような感じ
        "RC1RB3RA3RC1RA3" +  # 変化型
        
        # クライマックス部分
        "C1RC1RA3RB3RB3R" +  # 盛り上がり（キック強調）
        "A3RA3RC1RB3RC1R" +  # ハイハット連打感
        "C1RA3B3RA3C1RA3" +  # リズミカルな展開
        "B3RC1RB3RC1RA3R" +  # フィル効果
        
        # フィナーレ
        "C1RA3RC1RA3B3R" +  # 基本パターンに戻る
        "C1RA3B3RC1RA3R" +  # 微妙な変化
        "C1RC1RA3B3RC1R" +  # フィルインの導入
        "C1RB3RA3C1RRR",    # 終結パターン
        
        "N",  # トーンタイプ: Noise
        "6666666666666666",  # ボリューム (均一で適度な強さに)
        "N",  # エフェクト: None - クリアな音質
        16    # スピード - メインメロディーとベースに合わせて軽快に
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
