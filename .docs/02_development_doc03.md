# クラス図 （開発中）

実装していく間に増えるかもしれないので、覚えていたらここに追加していく。

## 要件

1. Python >=3.11 の予定。
2. LSFが使える環境で、`bjobs` および `bsub` コマンドがCLIで使える。Pythonならsubprocessで呼び出せる。バージョンは現状不明。
3. GitLabが使える環境で、GitLab APIが使える。Pythonなら `requests` モジュールで呼び出せる。詳細はこれからやる。
4. データベースはPythonの `sqlite3` モジュールで管理する。データベース設計はこれからやる。

## Phase 1-(a)

まずはRunnerInterfaceを作る。

```mermaid
classDiagram
    class ExperimentManager {
        -db_manager: DatabaseManager
        -runners: dict~str, RunnerInterface~
        +check_status(id: str) -> Result~Status, str~
    }

    class RunnerInterface {
        <<abstract>>
        -interface_name: Literal["Runner"]
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    class JobStatus {
        <<abstract>>
    }

    class JobRunner {
        <<abstract>>
    }

    class DatabaseManager {
        -db: JobDatabase
        +get_record(id: str) -> Result~Record, str~
        +create_record(new_record: NewRecord) -> Result~str, str~
        +update_record(id: str, record: Record) -> Result~str, str~
    }

    ExperimentManager "1" --> "1" DatabaseManager
    ExperimentManager "1" --> "*" RunnerInterface
    RunnerInterface "1" --> "*" JobRunner
    RunnerInterface "1" ..> "*" JobStatus
    DatabaseManager "1" --> "1" JobDatabase
```

## Phase 1-(b)

RunnerInterfaceとの連携を中心に、ExperimentManagerを拡張する。

```mermaid
classDiagram
    class ExperimentManager {
        -db_manager: DatabaseManager
        -runners: dict~str, RunnerInterface~
        -inputBuilders: List~InputBuilder~
        +check_status(id: str) -> Result~Status, str~
        +buildInput()
        +createRecord()
        +submitJob()
    }

    class DatabaseManager {
        -db: JobDatabase
        +get_record(id: str) -> Result~Record, str~
        +create_record(new_record: NewRecord) -> Result~str, str~
        +update_record(id: str, record: Record) -> Result~str, str~
    }

    class InputBuilder {
        <<abstract>>
        -config: dict
        -templatePath: str
        +build()
    }

    class RunnerInterface {
        <<abstract>>
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    ExperimentManager "1" --> "*" InputBuilder
    ExperimentManager "1" --> "1" DatabaseManager
    ExperimentManager "1" --> "*" RunnerInterface
    DatabaseManager "1" --> "1" JobDatabase
    RunnerInterface "1" --> "*" JobRunner
```

## Phase 1-(c)

LSFとの連携を中心に、ExperimentManagerを拡張する。

```mermaid
classDiagram
    class ExperimentManager {
        -db_manager: DatabaseManager
        -runners: dict~str, RunnerInterface~
        -inputBuilders: List~InputBuilder~
        +check_status(id: str) -> Result~Status, str~
        +buildInput()
        +createRecord()
        +submitJob()
    }

    class DatabaseManager {
        -db: JobDatabase
        +get_record(id: str) -> Result~Record, str~
        +create_record(new_record: NewRecord) -> Result~str, str~
        +update_record(id: str, record: Record) -> Result~str, str~
    }

    class LSFInterface {
        -interface_name: Literal["LSF"]
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    ExperimentManager "1" --> "1" DatabaseManager
    ExperimentManager "1" --> "*" LSFInterface
    DatabaseManager "1" --> "1" JobDatabase
    LSFInterface "1" --> "1" LSF
```

## Phase 1-(d)

GitLabとの連携を中心に、ExperimentManagerを拡張する。

```mermaid
classDiagram
    class ExperimentManager {
        -db_manager: DatabaseManager
        -runners: dict~str, RunnerInterface~
        -inputBuilders: List~InputBuilder~
        -gitLabSync: GitLabSynchronizer
        +check_status(id: str) -> Result~Status, str~
        +buildInput()
        +createRecord()
        +submitJob()
    }

    class DatabaseManager {
        -db: JobDatabase
        +get_record(id: str) -> Result~Record, str~
        +create_record(new_record: NewRecord) -> Result~str, str~
        +update_record(id: str, record: Record) -> Result~str, str~
    }

    class GitLabSynchronizer {
        -repository: str
        -branch: str
        -credentials: dict
        +commit()
        +push()
    }

    class LSFInterface {
        -interface_name: Literal["LSF"]
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    ExperimentManager "1" --> "1" DatabaseManager
    ExperimentManager "1" --> "1" GitLabSynchronizer
    ExperimentManager "1" --> "*" LSFInterface
    DatabaseManager "1" --> "1" JobDatabase
    GitLabSynchronizer "1" --> "1" GitLab
    LSFInterface "1" --> "1" LSF
```

## Phase 1-(e)

InputBuilderとの連携を中心に、ExperimentManagerを拡張する。

```mermaid
classDiagram
    class ExperimentManager {
        -db_manager: DatabaseManager
        -runners: dict~str, RunnerInterface~
        -inputBuilders: List~InputBuilder~
        -gitLabSync: GitLabSynchronizer
        +check_status(id: str) -> Result~Status, str~
        +buildInput()
        +createRecord()
        +submitJob()
    }

    class DatabaseManager {
        -db: JobDatabase
        +get_record(id: str) -> Result~Record, str~
        +create_record(new_record: NewRecord) -> Result~str, str~
        +update_record(id: str, record: Record) -> Result~str, str~
    }

    class GitLabSynchronizer {
        -repository: str
        -branch: str
        -credentials: dict
        +commit()
        +push()
    }

    class InputBuilder {
        <<abstract>>
        -config: dict
        -templatePath: str
        +build()
    }

    class LSFInterface {
        -interface_name: Literal["LSF"]
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    ExperimentManager "1" --> "*" InputBuilder
    ExperimentManager "1" --> "1" DatabaseManager
    ExperimentManager "1" --> "1" GitLabSynchronizer
    ExperimentManager "1" --> "*" LSFInterface
    DatabaseManager "1" --> "1" JobDatabase
    GitLabSynchronizer "1" --> "1" GitLab
    LSFInterface "1" --> "1" LSF
```

このクラス図では、シーケンス図に示された主要なコンポーネント間の関係を表現しています。各クラスには、シーケンス図で示された主要な操作をメソッドとして含めています。また、クラス間の依存関係も矢印で示しています。

主な特徴：

- `ExperimentManager`は中心的なクラスとして、他のコンポーネントを統括します
- 各コンポーネントは単一責任の原則に従い、明確な役割を持っています
- 外部システム（DatabaseとGitLab）との連携は、それぞれ専用のマネージャークラスを通じて行われます
