-- Financial Credit Risk Analytics Schema Setup
-- PostgreSQL / MySQL Compatible DDL

DROP TABLE IF EXISTS loan_portfolio;

CREATE TABLE loan_portfolio (
    loan_id VARCHAR(20) PRIMARY KEY,
    borrower_id VARCHAR(20) NOT NULL,
    issue_date DATE NOT NULL,
    loan_amount NUMERIC(12,2) CHECK (loan_amount > 0),
    interest_rate NUMERIC(5,2) CHECK (interest_rate >= 0),
    grade VARCHAR(5) CHECK (grade IN ('A', 'B', 'C', 'D', 'E')),
    employment_length_years NUMERIC(4,1),
    home_ownership VARCHAR(20) CHECK (home_ownership IN ('MORTGAGE', 'RENT', 'OWN')),
    annual_income NUMERIC(12,2) CHECK (annual_income >= 0),
    dti_ratio NUMERIC(5,2) CHECK (dti_ratio >= 0),
    credit_score INT CHECK (credit_score BETWEEN 300 AND 850),
    loan_purpose VARCHAR(50),
    loan_status VARCHAR(40) NOT NULL,
    total_principal_paid NUMERIC(12,2) DEFAULT 0,
    total_interest_paid NUMERIC(12,2) DEFAULT 0,
    delinquency_2yrs INT DEFAULT 0
);

-- Indexes for Speed
CREATE INDEX idx_loan_grade ON loan_portfolio(grade);
CREATE INDEX idx_loan_issue_date ON loan_portfolio(issue_date);
CREATE INDEX idx_loan_status ON loan_portfolio(loan_status);
CREATE INDEX idx_loan_credit_score ON loan_portfolio(credit_score);
