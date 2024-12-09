# ComputationalOps

## Overview

- ComputationalOps is an enterprise-grade computational workflow management system designed for high-performance computing (HPC) environments. It provides robust job management, dependency tracking, and visualization capabilities while maintaining strict security standards for internal use.

- It applies the pipeline management, version management, and visualization features established in DevOps and MLOps to HPC environments.
   1. HPC job delivery
   2. Process driven optimization

## Core Features

### 1. Job Management & Control

- **LSF Integration**: Seamless integration with LSF (Load Sharing Facility) for job submission and monitoring
- **Automated Status Monitoring**: Asynchronous monitoring of job status at 15-minute intervals
- **Error Handling**: Automatic job termination on errors with comprehensive error reporting
- **Metadata Management**: SQLite-based metadata tracking with YAML export capabilities

### 2. Dependency Management

- **Tree-based Structure**: Git-like branching model for managing computational dependencies
- **Hierarchical Branching**: Support for user-defined branch names with hierarchical structures
- **Single Parent Model**: Clear lineage tracking with single-parent dependency relationships
- **Status Propagation**: Intelligent handling of dependent job states

### 3. Visualization & Monitoring

- **Task Scheduler View**: Real-time display of:
  - Job IDs
  - Branch names
  - Current status
  - Execution duration
- **Tree Visualization**: Interactive view of computational dependencies with:
  - Color-coded status indicators
  - Branch hierarchy display
  - Real-time updates

### 4. Enterprise Security Features

- **Internal GitLab Integration**: Secure synchronization with internal GitLab servers
- **File System Security**: Leverages existing file system permissions
- **Data Isolation**: No external server communication except authorized internal GitLab
- **Audit Trail**: Comprehensive logging with rotation support

## Technical Specifications

### System Requirements

- Python 3.11+
- LSF (bsub/bjobs) environment
- Internal GitLab instance
- SQLite database support

### Data Management

- **Version Control**: Git-based data management
- **Evidence Trail**: YAML database exports for team sharing
- **Logging**: Detailed logging with rotation capabilities
- **Type Safety**: Comprehensive type hinting implementation

## Benefits

### For Management

- **Visibility**: Clear oversight of computational resources and project progress
- **Compliance**: Built-in security measures and audit capabilities
- **Resource Optimization**: Better control over computational resource allocation

### For Teams

- **Collaboration**: Shared access to computation results via GitLab
- **Reproducibility**: Clear tracking of computational dependencies
- **Error Management**: Quick identification and resolution of failed computations

### For Individual Users

- **Workflow Management**: Easy management of complex computational dependencies
- **Status Monitoring**: Real-time visibility into job status
- **Branch Management**: Flexible organization of computational workflows

## Architecture Highlights

1. **Core System**
   - SQLite database for metadata
   - LSF interface for job management
   - Asynchronous status monitoring
   - Git-based version control

2. **Dependency System**
   - Tree-based relationship management
   - Branch naming and organization
   - Status propagation logic
   - Error handling mechanisms

3. **Visualization System**
   - Real-time status updates
   - Interactive tree visualization
   - Task scheduler interface
   - Color-coded status indicators

## Security Considerations

- All data remains within corporate infrastructure
- No external API dependencies
- Integration limited to internal GitLab servers
- Leverages existing system permissions

This system is designed to enhance computational workflow management while maintaining strict security standards and providing comprehensive visibility into computational processes.
