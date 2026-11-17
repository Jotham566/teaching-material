// Weekly work only. Major tests/projects retain their separate weighted marks.
export const waivedAssessments=new Set(['Q6','W06','Q7','W07','Q14','W14','Q15','W15']);
export const isWaived=assessment=>waivedAssessments.has(assessment);
