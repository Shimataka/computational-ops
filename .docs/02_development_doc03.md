# クラス図

実装していく間に増えるかもしれないので、覚えていたらここに追加していく。

## Phase 1-(a)

まずはLSFにおける `bjobs` コマンドをパースするツールを作る。

```mermaid
classDiagram
    class ExperimentManager {
        -db_manager: DatabaseManager
        -runners: dict~str, RunnerInterface~
        +check_status(id: str) -> Result~Status, str~
    }

    class RunnerInterface {
        <<abstract>>
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    class LSFInterface {
        -interface_name: Literal["LSF"]
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    class DatabaseManager {
        -db: JobDatabase
        +get_record(id: str) -> Result~Record, str~
        +create_record(new_record: NewRecord) -> Result~str, str~
        +update_record(id: str, record: Record) -> Result~str, str~
    }

    ExperimentManager "1" --> "1" DatabaseManager
    ExperimentManager "1" --> "*" RunnerInterface
    ExperimentManager "1" --> "*" LSFInterface
    RunnerInterface "1" <|-- "1" LSFInterface
    RunnerInterface "1" --> "*" JobRunner
    DatabaseManager "1" --> "1" JobDatabase
    LSFInterface "1" --> "1" LSF
    JobRunner "1" <|-- "1" LSF
```

## Phase 1-(b)

LSFとの連携を中心に、ExperimentManagerを拡張する。

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

    class RunnerInterface {
        <<abstract>>
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    class LSFInterface {
        -interface_name: Literal["LSF"]
        +submit_job(input_file: str) -> Result~str, str~
        +get_status(id: str) -> Result~Status, str~
    }

    ExperimentManager "1" --> "*" InputBuilder
    ExperimentManager "1" --> "1" DatabaseManager
    ExperimentManager "1" --> "1" GitLabSynchronizer
    ExperimentManager "1" --> "*" RunnerInterface
    ExperimentManager "1" --> "*" LSFInterface
    DatabaseManager "1" --> "1" JobDatabase
    GitLabSynchronizer "1" --> "1" GitLab
    RunnerInterface "1" --> "*" JobRunner
    RunnerInterface "1" <|-- "1" LSFInterface
    LSFInterface "1" --> "1" LSF
    JobRunner "1" <|-- "1" LSF
```

このクラス図では、シーケンス図に示された主要なコンポーネント間の関係を表現しています。各クラスには、シーケンス図で示された主要な操作をメソッドとして含めています。また、クラス間の依存関係も矢印で示しています。

主な特徴：

- `ExperimentManager`は中心的なクラスとして、他のコンポーネントを統括します
- 各コンポーネントは単一責任の原則に従い、明確な役割を持っています
- 外部システム（DatabaseとGitLab）との連携は、それぞれ専用のマネージャークラスを通じて行われます
