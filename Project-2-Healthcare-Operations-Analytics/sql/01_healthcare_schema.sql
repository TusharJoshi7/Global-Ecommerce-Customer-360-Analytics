-- Healthcare Operations Analytics Schema Setup
-- PostgreSQL / MySQL Compatible DDL

DROP TABLE IF EXISTS patient_admissions;

CREATE TABLE patient_admissions (
    admission_id VARCHAR(20) PRIMARY KEY,
    patient_id VARCHAR(20) NOT NULL,
    admission_date TIMESTAMP NOT NULL,
    discharge_date TIMESTAMP NOT NULL,
    age INT CHECK (age >= 0 AND age <= 120),
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female', 'Other')),
    department VARCHAR(50) NOT NULL,
    admission_type VARCHAR(30) NOT NULL,
    triage_level INT CHECK (triage_level BETWEEN 1 AND 5),
    wait_time_minutes INT CHECK (wait_time_minutes >= 0),
    length_of_stay_days NUMERIC(5,2) CHECK (length_of_stay_days >= 0),
    readmission_30d INT CHECK (readmission_30d IN (0, 1)),
    treatment_cost NUMERIC(10,2) CHECK (treatment_cost >= 0),
    insurance_provider VARCHAR(50),
    discharge_status VARCHAR(50),
    doctor_id VARCHAR(20)
);

-- Performance Indexes
CREATE INDEX idx_patient_dept ON patient_admissions(department);
CREATE INDEX idx_patient_adm_date ON patient_admissions(admission_date);
CREATE INDEX idx_patient_triage ON patient_admissions(triage_level);
CREATE INDEX idx_patient_readmission ON patient_admissions(readmission_30d);
