import tiledbvcf, tiledb, tiledb.cloud 



tiledb.cloud.login(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjViYmViMGMtZmZkMC00ODQ2LWE5MmUtYWQzYmVjM2YwMzkxIiwiU2VlZCI6NDA1MTM4MTgxNjMzNTQ3OCwiZXhwIjoxNjc1MjI3NTk5LCJpYXQiOjE2NzQxNDU1NTcsIm5iZiI6MTY3NDE0NTU1Nywic3ViIjoiemhhbmYifQ.PlcIMFs0C4OWgCVGsrbD8vdBlf-zS54_c2_1WH8pQ8k")
prof = tiledb.cloud.user_profile()
print(prof)



token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjViYmViMGMtZmZkMC00ODQ2LWE5MmUtYWQzYmVjM2YwMzkxIiwiU2VlZCI6NDA1MTM4MTgxNjMzNTQ3OCwiZXhwIjoxNjc1MjI3NTk5LCJpYXQiOjE2NzQxNDU1NTcsIm5iZiI6MTY3NDE0NTU1Nywic3ViIjoiemhhbmYifQ.PlcIMFs0C4OWgCVGsrbD8vdBlf-zS54_c2_1WH8pQ8k"

cfg = {"tiledb_config": ["rest.token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjViYmViMGMtZmZkMC00ODQ2LWE5MmUtYWQzYmVjM2YwMzkxIiwiU2VlZCI6NDA1MTM4MTgxNjMzNTQ3OCwiZXhwIjoxNjc1MjI3NTk5LCJpYXQiOjE2NzQxNDU1NTcsIm5iZiI6MTY3NDE0NTU1Nywic3ViIjoiemhhbmYifQ.PlcIMFs0C4OWgCVGsrbD8vdBlf-zS54_c2_1WH8pQ8k"]}

uri = "tiledb://TileDB-Inc/vcf-1kg-nygc"
Array = tiledbvcf.Dataset(uri, mode= 'r', cfg=tiledbvcf.ReadConfig(**cfg))
print(Array.schema)