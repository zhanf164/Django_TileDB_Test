from django.shortcuts import render, redirect
from .models import User
from .forms import UserForm, RegionForm
import tiledbvcf
import tiledb.cloud
import pandas as pd
import json


# Create your views here.
def LoginPage(request):
    form = UserForm()
    context = {'form': form, 'errors': None}
    if request.method == "POST":
        #here somebody is trying to login, so validate that the username is real
        #I opt here to fetch the data from the request object itself, but in general, it would probably be best to fetch it
        #from the form object
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        try:
            user = User.objects.get(username=username)
            if user.password == password:
                return redirect('LandingPage')
            else:
                context = {'form': form, 'errors': "Incorrect Password"}
                return render(request, "LoginPage.html", context)
                
        except:
            #in this case the username does not exist in the DB
            context = {'form': form, 'errors': "Username does not exist in the DB"}
            return render(request, "LoginPage.html", context)
    return render(request, "LoginPage.html", context)


def LandingPage(request):
    #upon successful login here, we should go fetch the data from TileDB and return some context data to view
    form = RegionForm()
    context = {'form': form, 'data': None}
    #need to point TileDB to my credentials
    #not entirely sure this is actually necesary, but the TileDB guys said that we could use SSO for our users at a later date, so we will probably need this
    tiledb.cloud.login(token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjViYmViMGMtZmZkMC00ODQ2LWE5MmUtYWQzYmVjM2YwMzkxIiwiU2VlZCI6NDA1MTM4MTgxNjMzNTQ3OCwiZXhwIjoxNjc1MjI3NTk5LCJpYXQiOjE2NzQxNDU1NTcsIm5iZiI6MTY3NDE0NTU1Nywic3ViIjoiemhhbmYifQ.PlcIMFs0C4OWgCVGsrbD8vdBlf-zS54_c2_1WH8pQ8k")
    #checking that I am properly logged in
    prof = tiledb.cloud.user_profile()
    
    #Even when you do the above, I was still getting REST errors when trying to query the public data sets but after digging through the APIs I did find
    #that you can pass a ReadConfig object as a parameter to the Dataset() fetcher. Within it, you can pass standard TileDB parameters as a list of strings
    #with the format key=value . Found that here: https://docs.tiledb.com/main/integrations-and-extensions/genomics/population-genomics/api-reference/python
    #and for the tileDB config you can find possible parameters here: 
    cfg = {"tiledb_config": ["rest.token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjViYmViMGMtZmZkMC00ODQ2LWE5MmUtYWQzYmVjM2YwMzkxIiwiU2VlZCI6NDA1MTM4MTgxNjMzNTQ3OCwiZXhwIjoxNjc1MjI3NTk5LCJpYXQiOjE2NzQxNDU1NTcsIm5iZiI6MTY3NDE0NTU1Nywic3ViIjoiemhhbmYifQ.PlcIMFs0C4OWgCVGsrbD8vdBlf-zS54_c2_1WH8pQ8k"]}

    #instantiate connection to DB in read mode , passing our credentials to the ReadConfig object
    uri = "tiledb://TileDB-Inc/vcf-1kg-nygc"
    Array = tiledbvcf.Dataset(uri, mode= 'r', cfg=tiledbvcf.ReadConfig(**cfg))
    attributes = {}
    if request.method == "POST":
        #if user submits the webform, then fetch the data they filled in
        chrom = request.POST.get("chrom", "")
        start = request.POST.get("start", "")
        stop = request.POST.get("stop", "")
        #need to know samples in advance if you want to slice by them
        query_samples = ["HG00096", "HG00097", "HG00099", "HG00100", "HG00101", "HG00102", "HG00103", "HG00105", "HG00106", "HG00107", "HG00108", "HG00109", "HG00110", "HG00111", "HG00112", "HG00113", "HG00114", "HG00115", "HG00116", "HG00117", "HG00118", "HG00119", "HG00120", "HG00121", "HG00122", "HG00123", "HG00125", "HG00126", "HG00127", "HG00128", "HG00129", "HG00130", "HG00131", "HG00132", "HG00133", "HG00136", "HG00137", "HG00138", "HG00139", "HG00140", "HG00141", "HG00142", "HG00143", "HG00145", "HG00146", "HG00148", "HG00149", "HG00150", "HG00151", "HG00154", "HG00155", "HG00157", "HG00158", "HG00159", "HG00160", "HG00171", "HG00173", "HG00174", "HG00176", "HG00177", "HG00178", "HG00179", "HG00180", "HG00181", "HG00182", "HG00183", "HG00185", "HG00186", "HG00187", "HG00188", "HG00189", "HG00190", "HG00231", "HG00232", "HG00233", "HG00234", "HG00235", "HG00236", "HG00237", "HG00238", "HG00239", "HG00240", "HG00242", "HG00243", "HG00244", "HG00245", "HG00246", "HG00250", "HG00251", "HG00252", "HG00253", "HG00254", "HG00255", "HG00256", "HG00257", "HG00258", "HG00259", "HG00260", "HG00261", "HG00262"]
        query_attrs = ["sample_name", "contig", "pos_start", "pos_end", "alleles", "fmt_GT"]
        #build genomic region parameter using user defined values
        genomic_region = [f"{chrom}:{start}-{stop}"]
        df = Array.read(attrs=query_attrs, regions=genomic_region, samples=query_samples[:5])
        df_small = df.head(100) # head the dataframe for now since it can be huge. Pagination would be the future solution
        json_obj = df_small.reset_index().to_json(orient='records') # conver pandas df to json object for easy iteration within the Jinja template
        data = json.loads(json_obj) # convert to json
        print(data)
        context['data'] = data #store that in our context so we can fetch it later

        print(df)
        
    return render(request, "LandingPage.html", context)