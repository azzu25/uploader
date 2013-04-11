from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

Model = ['filename','md5hash','filesize','permalink','publishdate',
              'lastpublisheddate','uploadeddateTime','uploadeddatetime']

Company = ['companykey','previousticker','companyexchangecode','companyname','region',
           'country','yearendmon ','companyfootnote','companyid','name','ticker']

Analyst = ['analystcodelead ','analystnamelead','analystid','role','analystfirstnamelead','analystlastnamelead','analystemaillead']

Reference = ['modelcurrency', 'modelnote', 'transactionnote', 'restrictiontype', 'corporateaction', 
             'date', 'note', 'companynote', 'lastcorporateactiondate', 'lastcorporateactionnote']

Target = ['currentprice', 'pricecurrency', 'previouspricetarget', 'previouspricetargetwindow', 
          'previouspricetargetseton', 'investmentrating', 'investmentrecommendation', 
          'previousinvestmentrecommendation', 'investmentrecommendationchangenote', 'analystopinion', 
          'analystindustryview', 'volatilityrisk ', 'incomerating ', 'expectedreturn', 'expectedsharepricereturn', 
          'expecteddividendyield']
Timestamps = ['datetimemodeluploaded','datetimepublished ']

FinancialMeasures = ['sharesoutstandingbasic', 'sharesoutstandingdiluted', 'lastactualepsbasicq', 'lastactualepsdilutedq',
     'lastactualepsbasicy', 'lastactualepsdilutedy', 'lastactualepsbasic(gaap)q', 'lastactualepsdiluted(gaap)q',
      'lastactualepsbasic(gaap)y', 'lastactualepsdiluted(gaap)y', 'lastactualnetincome', 'revenue', 'ebit', 'ebitda', 'netincomebeforeextraordinary']

Root_Level_Keys = ['transactiontype','asondate', 'currentasondate']
Exclude_Keys = ['user', 'token']

def get_xml_data(post_data):
    xmldata = '<?xml version="1.0" encoding="UTF-8"?><Transaction>'
    other = '<Other>'
    models = '<Model>'
    modelid = post_data.get('modelid')
    if modelid:
        models = '<Model id="'+modelid+'">'
        del post_data['modelid']
    company = '<Company>'
    companyid = post_data.get('companyid')
    if companyid:
        company = '<Company id="'+companyid+'">'
        del post_data['companyid']
    analyst = '<Analysts>'
    analystid = post_data.get('analystid')
    if analystid:
        analyst = '<Analysts id="'+analystid+'">'
        del post_data['analystid']
    reference = '<Reference>'
    other = '<Other>'
    target = '<Target>'
    financial = '<FinancialMeasures>'
    transaction = ''
    for key,value in post_data.iteritems():
        key = key.lower()
        if key in Root_Level_Keys:
            transaction = transaction + '<'+key+'>'+value+'</'+key+'>'
        elif key in Model:
            models  = models+'<'+key+'>'+value+'</'+key+'>'
        elif key in Company:
            company  = company+'<'+key+'>'+value+'</'+key+'>'
        elif key in Reference:
            reference  = reference+'<'+key+'>'+value+'</'+key+'>'
        elif key in Target:
            target  = target+'<'+key+'>'+value+'</'+key+'>'
        elif key in Analyst:
            analyst  = analyst+'<'+key+'>'+value+'</'+key+'>'
        elif key in FinancialMeasures:
            financial  = financial+'<'+key+'>'+value+'</'+key+'>'
        elif key not in Exclude_Keys:
            other  = other+'<'+key+'>'+value+'</'+key+'>'
        
    models  = models+'</Model>'
    company = company+'</Company>'
    analyst = analyst + '</Analysts>'
    reference = reference + '</Reference>'
    other = other +'</Other>'
    target = target +'</Target>'
    financial = financial +'</FinancialMeasures>'
    xmldata = xmldata +transaction+models+company+analyst+reference+target+financial+other+'</Transaction>'   
    return xmldata

def dump_meta_data(post_data, user_name, fname):
    xmldata = str(get_xml_data(post_data))
    default_storage.save(user_name+'/'+fname+'.xml', ContentFile(xmldata))

    