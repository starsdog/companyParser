if (typeof json_path != 'undefined'){
    query_group();
} 
if (typeof group_name != 'undefined'){
    if(group_name=='all'){
        group_file='/companydata/group_relation/groupName_'+year+'.json';
        $.get(group_file,function(data){
            group_no_list=[];
            $.each(data, function (index, dict) {
                group_no_list.push(index);
            });   
            groupName_table.loadData(group_no_list);
            groupName_table.show(); 
        });
    }
    else{
        var set = new Set(group_name);
        var data=Array.from(set);

        console.log(data.length);
        if(data.length!=0){
            groupName_table.loadData(data);
            groupName_table.show(); 
        }
        else{
            $('#search_warning').css('display','inline-block');
        }
       
    }   
    
}   

function FineRecordItem(json){
    this.facility_name=json ? json.facility_name : null;
    this.penalty_date=json ? json.penalty_date : null;
    this.penalty_money=json ? json.penalty_money: null;
    this.transgress_law=json ? json.transgress_law: null;
    this.is_petition=json ? json.is_petition: null;
    this.petition_result=json ? json.petition_results: null;

    this.rawJSON = function () {
        return {
            'facility_name': this.facility_name,
            'penalty_date': this.penalty_date,
            'penalty_money': this.penalty_money,
            'transgress_law': this.transgress_law,
            'is_petition': this.is_petition,
            'petition_result': this.petition_result
        }
    }
}

function RelationItem(json){
    this.source=json ? json.source:null;
    this.taxcode_source=json ? json.taxcode_source:null;
    this.target=json ? json.target:null;
    this.taxcode_target=json ? json.taxcode_target:null;

    this.rawJSON = function () {
        return {
            'source': this.source,
            'taxcode_source': this.taxcode_source,
            "target": this.target,
            "taxcode_target": this.taxcode_target
        }
    }
}

function GroupInfo(json){
    this.group_name=json ? json.group_name:null;
    this.company_amount=json ? json.company_amount:null;
    this.has_fine=json ? json.has_fine:null;
    this.fine_company_amount=json ? json.fine_company_amount:null;
    this.fine_record_num=json ? json.fine_record_num:null;
    this.fine_penalty_amount=json ? json.fine_penalty_amount:null;
    this.group_no=json ? json.group_no:null;
    
    this.rawJSON = function () {
        return {
            'group_no': this.group_no,
            'group_name': this.group_name,
            'company_amount': this.company_amount,
            "has_fine": this.has_fine,
            "fine_company_amount": this.fine_company_amount,
            "fine_record_num": this.fine_record_num,
            "fine_penalty_amount": this.fine_penalty_amount
        }
    }
}

function TargetSourceItem(index, json){
    this.name=index;
    this.taxcode=json ? json.taxcode:null;
    
    source_list=json ? json.source_list:null;
    parsed_source = [];
    $.each(source_list, function(index, dict){
        row='母公司名稱: '+dict['name']+', 母公司持股: '+dict['holder']+'<br>';
        parsed_source.push(row);
    });
    this.source_list=parsed_source;
    
    this.rawJSON = function () {
        return {
            'name': this.source,
            'taxcode': this.taxcode,
            'source_list':this.source_list
        }
    }
}

function FineCompanyInfo(json){
    this.name=json ? json.name:null;
    this.taxcode=json ? json.taxcode:null;
    this.fine_num=json ? json.fine_num:null;
    this.penalty_amount=json ? json.penalty_amount:null;

    this.rawJSON = function () {
        return {
            'name': this.name,
            'taxcode': this.taxcode,
            "fine_num": this.fine_num,
            "penalty_amount": this.penalty_amount
        }
    }
}


function parseTargetSource(data){
    var parsed_target = [];
    $.each(data, function (index, dict) {
        target=new TargetSourceItem(index, dict);
        parsed_target.push(target);
    });

    return parsed_target;
}

function parseCompanyName(data) {
    var parsed_companys = [];
    $.each(data, function (index, dict) {
        parsed_companys.push(new RelationItem(dict));
    });

    return parsed_companys;
}

function parseFineRecord(data) {
    var parsed_records = [];
    $.each(data, function (index, dict) {
        parsed_records.push(new FineRecordItem(dict));
    });

    return parsed_records;
}

function parseFineCompany(data){
    var parsed_fine_companys = [];
    $.each(data, function (index, dict) {
        parsed_fine_companys.push(new FineCompanyInfo(dict));
    });

    return parsed_fine_companys;
}

function query_group(){
    console.log(json_path);
    $.get(json_path,function(data){
        summery=new GroupInfo(data['company_summery']);
        summery_table.loadData(summery);
        
        result = parseTargetSource(data['target_list']);
        var company_table_element = $('#table_company'); 
        company_table.companyItems=result;
        company_table.loadData(company_table_element, result);
        
        fine_company=parseFineCompany(data['fine_company_list']);
        var fine_company_table_element = $('#table_fine_company'); 
        fine_company_table.loadData(fine_company_table_element, fine_company);
        
        summery_table.show();
        company_table.show();
        if(summery['has_fine']==true)
            fine_company_table.show();
        else
            fine_company_table.hide();
    });
}

function query_fine_record(taxcode){
    $.get("/group/fine_record/"+taxcode, function(fine_record){
        var system_msg_index=fine_record.indexOf('<!-- Page cached');
        var clean_fine_record=fine_record;
        if (system_msg_index!=-1){
            clean_fine_record=fine_record.substring(0, system_msg_index);
        }
        
        var data=JSON.parse(clean_fine_record);
        result = parseFineRecord(data);
        var fine_record_table_element = $('#table_fine_record'); 
        fine_record_table.fineItems=result;
        fine_record_table.loadData(fine_record_table_element, result);
        fine_record_table.show();
        
        fine_company_table.hide();
    });    
}

