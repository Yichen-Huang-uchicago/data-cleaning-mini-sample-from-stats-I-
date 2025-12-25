# QA summary

- Rows: 13,092
- Columns: 16

## Missingness (top 10)

|                    |   missing_pct |   missing_n |
|:-------------------|--------------:|------------:|
| hh_has_electricity |         54.84 |        7180 |
| hh_head_educ_years |          0.44 |          57 |
| hh_head_age        |          0.17 |          22 |
| hhid               |          0    |           0 |
| cid                |          0    |           0 |
| vid                |          0    |           0 |
| uid                |          0    |           0 |
| does_hh_own        |          0    |           0 |
| does_hh_has_access |          0    |           0 |
| hh_any_od          |          0    |           0 |


## Binary checks

- `does_hh_own`: values=[0, 1]; invalid_n=0
- `does_hh_has_access`: values=[0, 1]; invalid_n=0
- `hh_any_od`: values=[0, 1]; invalid_n=0
- `any_treatment`: values=[0, 1]; invalid_n=0