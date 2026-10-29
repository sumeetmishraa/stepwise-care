export type RiskLevel = 'Low' | 'Medium' | 'High' | 'Critical'
export type Patient = {
  id: number; name: string; age: number; diagnosis: string; discharge_date: string; status: string;
  risk_level: RiskLevel; risk_score: number; readmission_probability: number; medications: string[];
  care_plan: { patient_summary?: string; medications?: {name:string;instruction:string}[]; follow_up_appointments?: {title:string;day:number;owner:string}[]; checkpoints?: {day:number;action:string;responsible_party:string}[]; review_required?: boolean };
  risk_factors: string[]; follow_up: string[]; notes: string;
}
export type Task = {id:number;patient_id:number;title:string;due_date:string;priority:string;status:string;owner:string}
export type Metrics = {total_patients:number;active_patients:number;needs_review:number;escalated:number;high_risk:number;open_tasks:number;average_risk:number;risk_distribution:{name:string;value:number}[]}
