# HAMARU Style 語学学習アプリ

ドイツ語 TOEFL 単語（660語）と英語構文（450語）を HAMARU 風ゲームUIで学習する PWA です。

## 使い方

1. `index.html` をブラウザで開く（または GitHub Pages の URL にアクセス）
2. メニュー上部で **🇩🇪 ドイツ語** / **🇬🇧 英語** を切り替え
3. カテゴリ → Part → Level を選んでプレイ

## GitHub にアップロードが必要なファイル

**最低限これら全部が必要です：**

| ファイル | 用途 |
|---------|------|
| `index.html` | アプリ本体 |
| `words-toefl-part1.js` | ドイツ語660語 |
| `words-english-grammar-part1.js` | 英語450語 |
| `data/toefl-part1.csv` | ドイツ語（バックアップ） |
| `data/english-grammar-part1.csv` | 英語（バックアップ） |
| `data/bgm.mp3` | BGM（10℃） |
| `data/10℃.mp3` | BGM（旧ファイル名・任意） |
| `data/Shooting-star-effect.mp4` | VFX |

`index.html` だけでは **0語** になり遊べません。

## スマホで遊ぶ（GitHub Pages）

**重要：スマホでは `file://`（ローカルファイル）は開けません。**

| 開き方 | Mac | スマホ |
|--------|-----|--------|
| Finder から `index.html` をダブルクリック | ✅ `file:///...` でOK | ❌ 不可 |
| GitHub Pages の URL | ✅ | ✅ **こちらを使う** |

公開 URL（例）:
```
https://kurenaru84-glitch.github.io/Deutsch-app/
```

リポジトリ Settings → Pages → Source: `main` ブランチ → Save  
数分後、上記 URL を **iPhone の Safari** で開く → 共有 → **ホーム画面に追加**

起動時の「タップして開始」を押すと BGM が鳴り、メニューが表示されます。
