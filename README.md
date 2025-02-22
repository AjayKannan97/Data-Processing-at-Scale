# Data Processing at Scale

## Overview
This repository contains coursework, projects, and assignments related to **Data Processing at Scale**, focusing on distributed data processing, optimization techniques, and large-scale data analytics.

## Course Details
- **Course**: Data Processing at Scale  
- **Institution**: Arizona State University (ASU)  
- **Topics Covered**:
  - Distributed Data Processing  
  - Apache Spark and MapReduce  
  - Data Partitioning & Indexing  
  - Query Optimization  
  - Parallel Databases  
  - Real-time Stream Processing  

## Technologies Used
- **Programming Languages**: Python, SQL, Java  
- **Frameworks & Tools**: Apache Spark, Hadoop, Hive, PostgreSQL, Pandas, NumPy  

## Repository Structure
```
Data-Processing-at-Scale/
│── datasets/                 # Sample datasets for analysis
│── notebooks/                # Jupyter notebooks with implementations
│── scripts/                  # Python/Java scripts for large-scale processing
│── reports/                  # Project reports and documentation
│── README.md                 # Project documentation
```

## Key Implementations
- **MapReduce Jobs**: Custom implementations for data aggregation and transformation.  
- **Apache Spark**: Utilized PySpark for large-scale data processing, including transformations and actions.  
- **SQL Query Optimization**: Improved query performance through indexing and execution plan analysis.  
- **Data Partitioning & Indexing**: Enhanced scalability through efficient partitioning techniques.  
- **Stream Processing**: Implemented Spark Streaming for real-time data analysis.  

## Setup Instructions
### Prerequisites
- Python 3.x  
- Java 8+  
- Apache Spark, Hadoop, PostgreSQL  
- Required Libraries:  
  ```bash
  pip install pandas numpy pyspark
  ```
  
### Running the Code
1. Clone the repository:
   ```bash
   git clone https://github.com/AjayKannan97/Data-Processing-at-Scale.git
   cd Data-Processing-at-Scale
   ```
2. Navigate to the appropriate directory (`notebooks/` or `scripts/`).  
3. Run the Spark job or Jupyter notebook:
   ```bash
   spark-submit scripts/example_spark_job.py
   ```
   or  
   ```bash
   jupyter notebook
   ```
4. View results and reports in the `reports/` directory.  

## Results & Observations
- **Optimized query execution** led to significant performance improvements.  
- **Apache Spark's in-memory processing** improved processing speed over traditional disk-based systems.  
- **Efficient data partitioning and indexing** enhanced scalability for large datasets.  

## Contributors
- **Ajay Kannan**  
- [Add other team members if applicable]  

## License
This project is for academic purposes. Please cite or reference appropriately if used.  

---
For any questions, contact **Ajay Kannan** at ajaykannan@gmail.com.  
