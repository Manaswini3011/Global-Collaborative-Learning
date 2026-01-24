-- Migration: Add 'submitted' status to assessments table
-- Run this SQL to update existing database schema

ALTER TABLE assessments 
MODIFY COLUMN status ENUM('draft', 'preview', 'finalized', 'submitted') DEFAULT 'draft';

-- Verify the change
-- SELECT COLUMN_TYPE FROM INFORMATION_SCHEMA.COLUMNS 
-- WHERE TABLE_SCHEMA = 'assessment_orchestrator' 
-- AND TABLE_NAME = 'assessments' 
-- AND COLUMN_NAME = 'status';

