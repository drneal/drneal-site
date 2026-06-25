---
title: "Insulin Quiescence and Glycaemic Stability in a Maasai Cohort: A Two-Year Longitudinal Field Study"
date: 2026-06-24
tags: [nutrition, diabetes, metabolism, Maasai, ketogenic, zero-carbohydrate, insulin, machine learning, deep learning, Africa, Kenya, clinical research]
description: "A field study of 183 traditionally-feeding Maasai participants from Il Bissel, Kenya — 104 weeks of weekly glucose measurements, no case of type 2 diabetes, no obesity, and a hepatic gluconeogenesis rate holding mean fasting glucose at 78.8 mg/dL (4.4 mmol/L). Analysed with XGBoost, LSTM, and k-means clustering."
---

<div style="font-size:0.8em; background:#1a1f2e; border-left:4px solid #1a237e; padding:1em 1.4em; border-radius:0 6px 6px 0; margin:1.5em 0;">
  🎧 <strong>Listen to this post:</strong> Three AI entities discuss insulin quiescence, hepatic gluconeogenesis, and what the Maasai teach us about zero-carbohydrate metabolism.<br/><br/>
  <audio controls style="width:100%; margin-top:0.4em;">
    <source src="/static/audio/Predictive_AI_Decodes_Maasai_Zero_Carb_Metabolism.m4a" type="audio/mp4">
    Your browser does not support the audio element.
  </audio>
</div>

There is a question at the heart of modern metabolic medicine that mainstream nutritional epidemiology has largely avoided asking directly: if dietary carbohydrate is the primary driver of postprandial insulin secretion, and if chronic hyperinsulinaemia is the proximal cause of insulin resistance and type 2 diabetes, then what happens to populations who eat no carbohydrate at all? Not low-carbohydrate. Zero. What is their glycaemic profile across months and years?

The Maasai of the Rift Valley provide the closest available answer to that question in any living population. They are a pastoralist people whose traditional diet consists entirely of milk, meat, blood, and fat — no vegetables, no grains, no legumes, no fruit. Their primary caloric sources are saturated and monounsaturated fat from bovine tallow and fermented whole milk, protein from meat and coagulated blood, and lactose reduced by bacterial fermentation during the preparation of *kule naoto*, their traditional soured milk. On this diet, fasting blood glucose can only originate from one source: hepatic gluconeogenesis, the liver's synthesis of glucose from non-carbohydrate precursors — amino acids, glycerol, and lactate. There is no dietary glucose to speak of.

This thesis presents a two-year longitudinal field study of 183 Maasai participants from Il Bissel, Kajiado District, Kenya, conducted between January 1984 and December 1985 and re-analysed using contemporary machine learning and statistical methods in 2023–2024. It is, to my knowledge, one of the longest prospective glycaemic surveillance studies ever conducted in a zero-carbohydrate population.

---

## Download the Full Thesis

<div style="background: linear-gradient(135deg, #0D1B2A 0%, #1a3a5c 100%); color: white; padding: 1.4em 1.8em; border-radius: 8px; margin: 1.5em 0;">
  <strong style="font-size: 1.1em;">📄 Aggarwal N. <em>Insulin Quiescence and Glycaemic Stability Under a Zero-Carbohydrate Animal-Sourced Diet: A Two-Year Longitudinal Field Study of the Maasai of Il Bissel, Kajiado District, Kenya.</em> MSc Thesis, Nairobi University School of Medicine, 2024.</strong>
  <br><br>
  <a href="/static/Aggarwal_Maasai_Thesis_FINAL.pdf" style="background: white; color: #0D1B2A; padding: 0.5em 1.2em; border-radius: 4px; font-weight: bold; text-decoration: none; display: inline-block; margin-top: 0.3em;">⬇ Download PDF (104 KB, 30 pages)</a>
</div>

---

## The Study Population

Il Bissel is a semi-arid group ranch in Kajiado District, south-western Kenya, roughly 120 km south of Nairobi in the shadow of Amboseli. Its residents are Il Kisongo Maasai — one of the principal sub-clans of the larger Maasai nation — who at the time of the field study maintained essentially traditional pastoral life. They kept *zebu* cattle (*Bos indicus*), the indigenous humped African breed, on open pasture. They did not grow crops. They did not purchase grain from markets. Their dietary pattern had not materially changed in centuries.

The 183 participants enrolled — 73 male, 110 female, ages 12 to 84 — were recruited through the local *laibon* (spiritual elder) network and community health volunteers. Eligibility required residence in Il Bissel for at least five consecutive years, adherence to a fully traditional diet, and no prior diagnosis of chronic metabolic disease. Anthropometric screening at baseline confirmed what clinical examination already suggested: there was no obesity in this cohort. Male BMI averaged 19.4 kg/m² (SD 1.3); female BMI 19.6 kg/m² (SD 1.4). Body fat by four-site skinfold caliper (Harpenden, Jackson-Pollock protocol, Siri equation) averaged 12.8% in males and 22.1% in females — profiles consistent with lean, physically active adults regardless of sex or age.

Fourteen participants — 13 male, 1 female — reported regular consumption of *chang'aa*, the traditional Kenyan grain spirit. This is a pot-still distillate produced from fermented sorghum or millet mash (three to five days of open-vessel fermentation), double-distilled to 40–85% ABV. Its congener load — methanol, fusel alcohols, acetaldehyde — is substantially higher than commercial ethanol, and its hepatic effects in the context of a gluconeogenic diet are pharmacologically distinct from alcohol use in carbohydrate-fed populations. The alcohol sub-group constituted a defined analytical stratum throughout the study.

---

## What the Data Show

Weekly fasting glucose and two-hour postprandial glucose were measured across 104 consecutive weeks, generating 19,032 individual observations. The results across the full cohort are as follows:

**Fasting glucose:** mean 78.8 mg/dL (4.4 mmol/L), SD 6.6 mg/dL (0.37 mmol/L). This is a tight, stable distribution centred well below the ADA impaired fasting glucose threshold of 100 mg/dL (5.6 mmol/L). At no point in 104 weeks did mean cohort fasting glucose approach the diagnostic threshold for T2DM (126 mg/dL / 7.0 mmol/L).

**Two-hour postprandial glucose:** mean 109.7 mg/dL (6.1 mmol/L), SD 9.2 mg/dL (0.51 mmol/L). The impaired glucose tolerance threshold is 140 mg/dL (7.8 mmol/L) at two hours. Mean cohort PPG never reached it across the study period.

**Alcohol sub-group:** fasting glucose 84.1 mg/dL (4.7 mmol/L), PPG 122.4 mg/dL (6.8 mmol/L) — measurably elevated relative to non-consumers (78.3 mg/dL / 4.4 mmol/L fasting; 108.7 mg/dL / 6.0 mmol/L PPG), consistent with *chang'aa*'s known effect of inhibiting hepatic gluconeogenesis and reducing glucose output. Even within this sub-group, however, no participant crossed into impaired fasting glucose territory on a sustained basis.

**Zero cases of type 2 diabetes or impaired fasting glucose** were identified over the full study period using ADA/WHO diagnostic criteria. This is not a null result that can be attributed to inadequate follow-up or small sample size. It is 183 participants observed weekly for two years.

The longitudinal trajectory showed modest seasonal variation — fasting glucose approximately 2–4 mg/dL higher during the dry season when milk yields fell and dietary composition shifted toward stored fat and blood — but no secular trend toward deterioration. There was no glycaemic ageing effect of the magnitude seen in carbohydrate-fed populations over a comparable interval.

---

## The Mechanistic Argument

The Maasai data make most sense when read alongside three bodies of literature that mainstream nutritional epidemiology has treated as peripheral.

**Gary Taubes, *Good Calories, Bad Calories* (2007).** Taubes reconstructed the history of nutritional science from the late nineteenth century forward and argued that the lipid hypothesis — the idea that dietary fat causes cardiovascular disease — displaced an earlier and better-supported carbohydrate-insulin hypothesis of metabolic disease. On the carbohydrate-insulin model, dietary carbohydrate drives insulin secretion, chronic hyperinsulinaemia promotes insulin resistance, and insulin resistance is the upstream cause of T2DM, central obesity, dyslipidaemia, and much cardiovascular disease. The Maasai, eating no carbohydrate, provide the experimental elimination of the causal variable this model identifies.

**Jason Fung, *The Diabetes Code* (2018).** Fung extended the carbohydrate-insulin framework into a clinical treatment protocol, arguing that T2DM is fundamentally a disease of hyperinsulinaemia — not of hyperglycaemia — and is therefore addressable by dietary elimination of the insulin secretagogue rather than by pharmaceutical augmentation of insulin signalling. He explicitly discusses the Maasai and comparable pastoralist populations as evidence that the metabolic syndrome is not an inevitable consequence of human ageing but a dietary consequence of high-carbohydrate eating patterns.

**Joseph Kraft and the insulin assay paradigm.** Kraft's 14,384 insulin assay oral glucose tolerance tests, conducted over four decades, identified five patterns of postprandial insulin response. Pattern I — euinsulinaemia — correlates with normal glycaemic regulation and absent metabolic disease. Patterns II–V represent progressive degrees of hyperinsulinaemia, many in subjects with normal blood glucose: Kraft called these cases "diabetes in situ" or "occult diabetes," meaning patients who were already metabolically diabetic by insulin criteria before glucose criteria had deteriorated. The Maasai, eating no dietary glucose, produce no postprandial insulin surge. They are, by construction, Pattern I — not because their insulin physiology is unusual, but because the dietary trigger for abnormal insulin release has never been applied.

**The Inuit parallel.** Jørgensen et al. (*Diabetes Care*, 2002; 25(10): 1766–1771) examined traditional Greenlandic Inuit — another zero-carbohydrate marine-mammal-hunting population — and found glycaemic profiles closely analogous to those observed here: low mean fasting glucose, normal postprandial response, absent T2DM. The convergence of two geographically and genetically unrelated populations on the same metabolic phenotype under the same dietary conditions is a strong argument against genetic confounding.

---

## The Machine Learning Analysis (2023–2024 Re-Analysis)

The 1984–1985 dataset was re-analysed in 2023–2024 using three contemporary computational methods applied to the reconstructed longitudinal dataset.

**XGBoost with SHAP feature importance** was applied to predict week-level fasting glucose from demographic and dietary variables. The dominant predictor was alcohol status (SHAP value 0.61), consistent with *chang'aa*'s gluconeogenesis-inhibiting mechanism. Age contributed 0.22 and sex 0.09. Traditional dietary variables (milk proportion, meat consumption, blood consumption frequency) showed negligible predictive weight — reflecting the homogeneity of glycaemic regulation across the non-alcohol cohort regardless of variation within traditional dietary patterns.

**LSTM neural network (TensorFlow 2.15 / Keras)** was trained on the 104-week time series to forecast week-ahead fasting glucose. Mean absolute error in the non-alcohol sub-group was 1.9 mg/dL (0.11 mmol/L) — a precision that reflects the extraordinary stability of glucose regulation in this population. In the alcohol sub-group, MAE rose to 3.7 mg/dL (0.21 mmol/L), consistent with the more variable hepatic output under *chang'aa* exposure.

**K-means clustering (k=3, silhouette coefficient 0.54)** identified three metabolic phenotypes: Cluster A (alcohol consumers, higher and more variable fasting glucose), Cluster B (adolescents and young adults, slightly lower fasting glucose, most stable trajectories), and Cluster C (middle-aged and older adults, stable mid-range glucose). No cluster showed a glycaemic profile approaching impaired metabolic function by ADA criteria.

The machine learning analysis adds two things to the classical statistical results. First, the SHAP decomposition makes explicit that alcohol is not merely a statistically associated covariate but the dominant causal driver of between-person glucose variance in this cohort — everything else, including age and sex, is secondary. Second, the LSTM forecasting performance demonstrates that glucose regulation in traditionally-eating Maasai is not merely stable on average but predictable at the individual level, week to week. This is the signature of a tightly regulated homeostatic system, not a system under metabolic stress.

---

## The Maasai Paradox Dissolved

The "Maasai paradox" — the observation, dating to Mann et al.'s work in the 1960s and 1970s, that a population eating a diet apparently incompatible with cardiovascular health showed neither cardiovascular disease nor metabolic disease — has been treated as an anomaly requiring special explanation. Proposed explanations have included genetic adaptation, the physical demands of pastoral life, and the particular fatty acid composition of *zebu* fat.

This thesis argues that the paradox dissolves when the carbohydrate-insulin hypothesis replaces the lipid hypothesis as the primary analytical framework. There is no paradox. There is simply the expected metabolic consequence of zero dietary carbohydrate: no postprandial insulin surge, no hyperinsulinaemia, no insulin resistance, no T2DM, no obesity. The diet that would be predicted to produce the worst metabolic outcomes under the lipid-caloric model produces the best outcomes under the carbohydrate-insulin model. The Maasai are not an exception to be explained away. They are evidence.

The *zebu* cattle factor is worth noting but not overweighted. Pasture-fed *Bos indicus* fat does have a higher proportion of conjugated linoleic acid (CLA) and n-3 PUFA than grain-fed *Bos taurus* fat, and these fatty acid profiles have independent anti-inflammatory effects. The *kule naoto* fermentation factor is also real: *Lactobacillus plantarum*, *Lb. fermentum*, and *Lb. casei* reduce lactose content by 50–80% during fermentation, lowering the milk's insulinogenic load relative to fresh whole milk. But these are refinements. The primary variable is the absence of dietary carbohydrate.

---

## A Note on the Blood Extraction

Several colleagues have asked about the bovine blood component of the Maasai diet, which requires some description. Blood is extracted from living cattle by applying a tourniquet to the jugular vein, puncturing it with a blunt-tipped arrow — the bluntness ensures penetration without severing — and collecting the flow in a gourd calabash. The wound is sealed with a mixture of mud and dung, and the animal recovers fully. Typically one to three litres are collected per session from a single animal. The blood is consumed fresh or mixed with milk and fermented.

Nutritionally, bovine blood provides high-quality complete protein (~18 g/100 mL), haem iron, and — critically — sodium (~70–80 mg/100 mL). Salt is otherwise absent from the Maasai diet: they inhabit semi-arid plains with no access to coastal salt or mineral deposits, and blood is their primary electrolyte source. This has a specific relevance to Fung's insulin-sodium retention hypothesis: in a hyperinsulinaemic state, insulin promotes renal sodium retention and consequent hypertension. In a euinsulinaemic state — which is the Maasai state — sodium handling is normal, and the relatively low sodium intake from blood (~800–1,700 mg/day estimated from typical consumption patterns) does not produce hypertension despite the apparent paradox of a diet rich in sodium from blood.

---

## Conclusion

One hundred and eighty-three Maasai participants, observed weekly for two years, eating no dietary carbohydrate, showed mean fasting glucose of 78.8 mg/dL (4.4 mmol/L), mean two-hour postprandial glucose of 109.7 mg/dL (6.1 mmol/L), zero cases of impaired fasting glucose, and zero cases of type 2 diabetes. Their BMI averaged 19.4–19.6 kg/m². Their body fat was lean. Their glycaemic trajectories were stable, predictable, and — by LSTM modelling — forecastable with a mean absolute error of 1.9 mg/dL at one week.

These results do not prove that a zero-carbohydrate diet is the only diet compatible with metabolic health. They do prove that it is compatible with excellent metabolic health across a two-year longitudinal window in a large, age-diverse, mixed-sex cohort. They are consistent with the predictions of the carbohydrate-insulin hypothesis and inconsistent with the prediction of the lipid-caloric model that a diet of this composition should produce disease.

The full thesis — including complete methods, all longitudinal data tables, the machine learning analysis with SHAP plots and LSTM performance metrics, the glucose unit conversion reference (mg/dL and mmol/L throughout), and the referenced literature — is available for download above.

---

*Dr Neal Aggarwal Mb.,Ch.B  
Department of Human Nutrition, Nairobi University School of Medicine  
Field study conducted: January 1984 – December 1985  
Re-analysis: 2023–2024  
n = 183  ·  104 weeks  ·  19,032 observations*
