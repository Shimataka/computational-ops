# computational-ops

[English version](.docs/01_README_en.md)

## 概要

ComputationalOpsは、高性能計算環境向けに設計された企業グレードの計算ワークフロー管理システムです。堅牢なジョブ管理、依存関係の追跡、可視化機能を提供しながら、社内利用に適した厳格なセキュリティ基準を維持します。

## 主要機能

### 1. ジョブ管理・制御

- **LSF連携**: LSF（Load Sharing Facility）とのシームレスな統合によるジョブ投入と監視
- **自動状態監視**: 15分間隔での非同期ジョブステータス監視
- **エラー処理**: 包括的なエラーレポートと自動ジョブ終了機能
- **メタデータ管理**: SQLiteベースのメタデータ追跡（YAML形式でのエクスポート機能付き）

### 2. 依存関係管理

- **ツリーベース構造**: Git風の分岐モデルによる計算依存関係の管理
- **階層的分岐**: ユーザー定義の階層構造を持つブランチ名のサポート
- **単一親モデル**: 単一親による明確な系統追跡
- **状態伝播**: 依存ジョブの状態を考慮したインテリジェントな処理

### 3. 可視化・監視

- **タスクスケジューラビュー**: リアルタイム表示
  - ジョブID
  - ブランチ名
  - 現在の状態
  - 実行時間
- **ツリー可視化**: 計算依存関係のインタラクティブビュー
  - 状態のカラーコード化
  - ブランチ階層表示
  - リアルタイム更新

### 4. エンタープライズセキュリティ機能

- **社内GitLab連携**: 社内GitLabサーバーとの安全な同期
- **ファイルシステムセキュリティ**: 既存のファイルシステム権限の活用
- **データ分離**: 認可された社内GitLab以外の外部サーバー通信なし
- **監査証跡**: ローテーション機能付きの包括的なログ記録

## 技術仕様

### システム要件

- Python 3.11以上
- LSF（bsub/bjobs）環境
- 社内GitLabインスタンス
- SQLiteデータベースサポート

### データ管理

- **バージョン管理**: Gitベースのデータ管理
- **エビデンス管理**: チーム共有用のYAMLデータベースエクスポート
- **ログ記録**: ローテーション機能付きの詳細ログ
- **型安全性**: 包括的な型ヒントの実装

## 導入メリット

### 経営管理層向け

- **可視性**: 計算リソースとプロジェクト進捗の明確な把握
- **コンプライアンス**: 組み込みのセキュリティ対策と監査機能
- **リソース最適化**: 計算リソースの配分管理の向上

### チーム向け

- **コラボレーション**: GitLabを通じた計算結果の共有
- **再現性**: 計算依存関係の明確な追跡
- **エラー管理**: 失敗した計算の迅速な特定と解決

### 個人ユーザー向け

- **ワークフロー管理**: 複雑な計算依存関係の容易な管理
- **状態監視**: ジョブ状態のリアルタイム可視化
- **ブランチ管理**: 計算ワークフローの柔軟な整理

## アーキテクチャのポイント

1. **コアシステム**
   - メタデータ用SQLiteデータベース
   - ジョブ管理用LSFインターフェース
   - 非同期状態監視
   - Gitベースのバージョン管理

2. **依存関係システム**
   - ツリーベースの関係管理
   - ブランチの命名と整理
   - 状態伝播ロジック
   - エラー処理メカニズム

3. **可視化システム**
   - リアルタイム状態更新
   - インタラクティブなツリー可視化
   - タスクスケジューラインターフェース
   - 状態のカラーコード化

## セキュリティ考慮事項

- すべてのデータを社内インフラ内に保持
- 外部APIへの依存なし
- 社内GitLabサーバーのみに連携を限定
- 既存のシステム権限を活用

本システムは、厳格なセキュリティ基準を維持しながら、計算プロセスの包括的な可視性を提供し、計算ワークフロー管理を強化するように設計されています。

## How to import template

1. このリポジトリからテンプレートを作成( `Use this template` ボタンから)、
または `.git` 以外の中身を新しいリポジトリにコピーしてください。
1. 目的に合わせて調整してください。
    - Pythonの場合、[Python開発環境の場合](.settings/templates/python/template.md)を参照してください。
    - Rustの場合、[Rust開発環境の場合](.settings/templates/rust/template.md)を参照してください。
    - Gitによるバージョン管理を行う場合、[Git環境の場合](.settings/templates/git/template.md)を参照してください。
    - その他の言語は考慮されていません。希望がある場合はissueにてお願いします。

## Technology stack

| カテゴリー | ツール |
| --- | --- |
| IDE設定 | [EditorConfig](https://editorconfig.org/) |
| CI/CD | [GitHub Actions](https://github.com/features/actions) |
| コードレビュー | [reviewdog](https://github.com/reviewdog/reviewdog) |
| リリース | [semantic-release](https://semantic-release.gitbook.io/semantic-release/) |
| 依存性更新 | [Dependabot](https://docs.github.com/ja/code-security/dependabot) |
| Git commit messages | [commitlint](https://commitlint.js.org/) |
| Credentials | [Secretlint](https://github.com/secretlint/secretlint) |
| Markdown | [markdownlint-cli](https://github.com/igorshubovych/markdownlint-cli) |
| YAML | [yamllint](https://yamllint.readthedocs.io/) |
| GitHub Actions Workflow | [actionlint](https://github.com/rhysd/actionlint) |
