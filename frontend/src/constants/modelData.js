
export const modelWeights = {
  "past_disorder": -0.301195,
  "diagnosed_flag": 0.10308,
  "productivity_impact": 2.138763,
  "family_history": 0.461901,
  "knows_benefits": -0.110507,
  "prev_employer_support": 0.112029,
  "fear_consequences": -2.764035,
  "leave_easiness": 0.165262,
  "support_index": 1.60188,
  "stigma_index": -1.372303
};
export const modelIntercept = -2.68678323641554;
export const syntheticProfiles = [
  {
    "id": "profile_01",
    "name": "The Guarded Professional",
    "description": "High performance but high fear of career impact. Reluctant to disclose due to perceived corporate stigma.",
    "inputs": {
      "past_disorder": 1,
      "diagnosed_flag": 0,
      "productivity_impact": 0.8,
      "family_history": 0,
      "knows_benefits": 0.2,
      "prev_employer_support": 0.1,
      "fear_consequences": 1,
      "leave_easiness": 0.2,
      "support_index": 0.1,
      "stigma_index": 0.9
    },
    "expected_status": "Critical Risk"
  },
  {
    "id": "profile_02",
    "name": "The Empowered Ally",
    "description": "Strong trust in leadership and high awareness of company benefits. Feels safe discussing mental health.",
    "inputs": {
      "past_disorder": 0,
      "diagnosed_flag": 0,
      "productivity_impact": 0.2,
      "family_history": 1,
      "knows_benefits": 1,
      "prev_employer_support": 0.8,
      "fear_consequences": 0,
      "leave_easiness": 0.9,
      "support_index": 0.9,
      "stigma_index": 0.1
    },
    "expected_status": "High Well-being"
  },
  {
    "id": "profile_03",
    "name": "The Uncertain Contributor",
    "description": "The perfect 'What-If' case. Moderate stigma and low benefit awareness.",
    "inputs": {
      "past_disorder": 0,
      "diagnosed_flag": 0,
      "productivity_impact": 0.5,
      "family_history": 0,
      "knows_benefits": 0.3,
      "prev_employer_support": 0.4,
      "fear_consequences": 0.5,
      "leave_easiness": 0.5,
      "support_index": 0.4,
      "stigma_index": 0.5
    },
    "expected_status": "Moderate Risk"
  }
];
