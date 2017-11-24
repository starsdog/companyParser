function GroupItem(json) {
    this.group_no = json ? json.group_no : null;
    this.group_name_list = json ? json.group_name_list : null;
    this.has_fine_record = json ? json.has_fine_record : null;
    this.has_discount = json ? json.has_discount : false;
    this.fine_money_amount =  json ? json.fine_money_amount : false;
    this.fine_record_count =  json ? json.fine_record_count : false;
    if (this.has_fine_record)
        this.has_fine_record='v';
    else
        this.has_fine_record='';

    if (this.has_discount)
        this.has_discount='v';
    else
        this.has_discount='';

    this.rawJSON = function () {
        return {
            'group_no': this.group_no,
            'group_name_list': this.group_name_list,
            "has_fine_record": this.has_fine_record,
            "has_discount": this.has_discount
        }
    }
}

function CompanyItem(json){
    this.company_name=json ? json.name : null;
    this.taxcode=json ? json.taxcode : null;
    this.has_discount= json ? json.taxdiscount : false;
    this.fine_record=json ? json.fine_record: null;
    if ('{}' === JSON.stringify(this.fine_record)){
        this.has_fine_record='';
        this.fine_money_amount=0;
        this.fine_record_count=0;
    }
    else{
        this.has_fine_record='v';
        this.fine_money_amount =  json ? json.fine_record.money_amount : false;
        this.fine_record_count =  json ? json.fine_record.record_count: false;
    }

    if (this.has_discount)
        this.has_discount='v';
    else
        this.has_discount='';

    this.rawJSON = function () {
        return {
            'company_name': this.company_name,
            'taxcode': this.taxcode,
            'has_fine_record': this.has_fine_record, 
            'has_discount': this.has_discount,
            "fine_money_amount": this.fine_money_amount,
            "fine_record_count": this.fine_record_count
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

function parseGroups(data) {
    var parsed_groups = [];
    var parsed_company = {};
    var parsed_record = {};
    $.each(data, function (index, dict) {
        parsed_groups.push(new GroupItem(dict));
        var parsed_company_list =[];
        
        $.each(dict['company_list'], function (index, dict) {
            var parsed_record_list =[];
            parsed_company_list.push(new CompanyItem(dict));
            $.each(dict['fine_record']['record'], function (index, dict) {
                parsed_record_list.push(new FineRecordItem(dict))
            });
            parsed_record[dict['taxcode']]=parsed_record_list;    
        });  

        parsed_company[dict['group_no']]=parsed_company_list;
       
    });

    return [parsed_groups, parsed_company, parsed_record];
}

var group_api={
    
    'login': function(){
        req_ajax({
            url: web_url+"/login",
            data: {
                "username": 'ling'
            },
            success: function(data){

            },
            error: function(data){

            }    
        })    
    },

    'getMsg': function(){
        req_ajax_get({
            url: web_url+"/getMsg",
            success: function(data){
                console.log(data);
                $('#test_msg').text(data);
            },
            error: function(data){

            }    
        })    
    },

    'hideall': function(){
        $('#group_query_area').css('display','none');
        $('#table_query_body').empty();
        $('#company_name').val('');
        group_table.hide();
        company_table.hide();
        thaubing_group_table.hide();
        thaubing_company_table.hide();
        thaubing_record_table.hide();
        taxdiscount_group_table.hide();
        taxdiscount_company_table.hide();
    },

    'query': function(){
        this.hideall();
        if ($('#relation_graph').is(":checked")){
            console.log("go relation_graph");
            this.query_list(false);
        }
        else if ($('#relation_query').is(":checked")){
            console.log("go relation_query");
            $('#group_query_area').css('display','inline-block');
        } 
        else if ($('#thaubing').is(":checked")){
            console.log("go thaubing");
            this.query_list(true);
        } 
        else if ($('#tax_discount').is(":checked")){
            this.query_discountlist(true);
        }    
    },

    'query_discountlist':function(){
         var year=$('#year').val();
        
        req_ajax({
            url: web_url+"/group/list/query",
            data: {
                "year": year
            },
            success: function(data){
                result = parseGroups(data);
                var taxdiscount_group_element = $('#taxdiscount_group');
                taxdiscount_group_table.groupItems=result[0];
                taxdiscount_company_table.companyItems=result[1];
                
                taxdiscount_group_table.loadData(taxdiscount_group_element, result[0]);
                taxdiscount_group_table.show();
                taxdiscount_company_table.hide();
            },    
             error: function (data) {
            }
        }); 
    },

    'query_list':function(with_fine_record){
        var year=$('#year').val();
        
        req_ajax({
            url: web_url+"/group/list/query",
            data: {
                "year": year
            },
            success: function(data){
                if (with_fine_record){
                    result = parseGroups(data);
                    var thaubing_group_element = $('#thaubing_group');
                    thaubing_group_table.groupItems=result[0];
                    thaubing_company_table.companyItems=result[1];
                    thaubing_record_table.fineRecordItems=result[2];
                    
                    thaubing_group_table.loadData(thaubing_group_element, result[0]);
                    thaubing_group_table.show();
                    thaubing_company_table.hide();

                }
                else{
                    result = parseGroups(data);
                    var group_table_element = $('#table_group');
                    group_table.groupItems=result[0];
                    company_table.companyItems=result[1];
                    group_table.loadData(group_table_element, result[0]);
                    group_table.show();
                    company_table.hide();
                }
            },
            error: function (data) {
            }
        }); 
    },

    'query_parent':function(){
        var company_name=$('#company_name').val();
        
        req_ajax({
            url: web_url+"/group/parent/query",
            data: {
                "company_name": company_name
            },
            success: function(data){
                $('#table_query_body').empty();
                if (data['errorCode']!=0){
                    $('#query_error_msg').text(data['error']);
                }
                else{
                    $('#query_error_msg').text('');
                    var row='<tr role="row" class="odd">'
                    row +='<td class="sorting_1">'+data['result'][0]['group_no']+'</td>'
                    row +='<td class="sorting_1">'+data['result'][0]['group_name']+'</td>'
                    row += '</tr>'
                    $('#table_query_body').append(row);
                }
               
            },
            error: function (data) {


            }
        }); 
    }    

}

var company_table={
    'companyItems': {},
    'table_element': $('#table_company'),

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "taxcode"},
                {data: "company_name"}
            ],
            order: [[0, 'asc']],
            dom: 'Bfrtlip',
            columnDefs: [],
            buttons:[{
                text: "<i class='glyphicon glyphicon-menu-left'></i>回上頁" ,
                action: function (e, dt, node, config) {
                    company_table.hide();
                    group_table.show();
                }
            }, 
            {
                text: "<i class='glyphicon glyphicon-download-alt'></i>下載zip" ,
                action: function (e, dt, node, config) {
                
                }             
            }]
        })    
    },      

    'loadData': function (data) {
        this.table_element.DataTable().clear();
        this.table_element.DataTable().rows.add(this.companyItems[data]).draw();
    },  

    'show': function(){
       $('#table_company_area').css('display','inline-block');
    },

    'hide': function(){
        $('#table_company_area').css('display','none');
    }
}

var group_table={
    'groupItems':[],

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "group_no"},
                {data: "group_name_list"}
            ],
            order: [[0, 'asc']],
            dom: 'Bfrtlip',
            columnDefs: [{
                'targets': 0,
                'searchable': true,
                'orderable': true,
                'width': '1%',
                'render': function (data, type, full, meta) {
                    return '<td ><button class="btn btn-link" onclick="company_table.loadData(\''+data+'\'); company_table.show(); group_table.hide(); return false">'+data+'</button></td>';
                }
            }],
            buttons:[]
        })    
    },        

    'loadData': function (table, data) {
        table.DataTable().clear();
        table.DataTable().rows.add(data).draw();
    },

    'show': function () {
       $('#table_group_area').css('display','inline-block');
    },

    'hide': function(){
        $('#table_group_area').css('display','none');
    }
}


var thaubing_group_table={
    'groupItems':[],

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "group_no"},
                {data: "group_name_list"},
                {data: "has_fine_record"},
                {data: "has_discount"},
                {data: "fine_record_count"},
                {data: "fine_money_amount"}
            ],
            order: [[2, 'desc']],
            dom: 'Bfrtlip',
            columnDefs: [{
                'targets': 0,
                'searchable': true,
                'orderable': true,
                'width': '1%',
                'render': function (data, type, full, meta) {
                    return '<td ><button class="btn btn-link" onclick="thaubing_company_table.loadData(\''+data+'\'); thaubing_company_table.show(); thaubing_group_table.hide(); return false">'+data+'</button></td>';
                }
            }],
            buttons:[]
        })    
    },        

    'loadData': function (table, data) {
        table.DataTable().clear();
        table.DataTable().rows.add(data).draw();
    },

    'show': function () {
       $('#thaubing_group_area').css('display','inline-block');
    },

    'hide': function(){
        $('#thaubing_group_area').css('display','none');
    }
}

var thaubing_company_table={
    'companyItems': {},
    'table_element': $('#thaubing_company'),

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "taxcode"},
                {data: "company_name"},
                {data: "has_fine_record"},
                {data: "has_discount"},
                {data: "fine_record_count"},
                {data: "fine_money_amount"}

            ],
            order: [[2, 'desc']],
            dom: 'Bfrtlip',
            columnDefs: [{
                'targets': 0,
                'searchable': true,
                'orderable': true,
                'width': '1%',
                'render': function (data, type, full, meta) {
                        return '<td ><button class="btn btn-link" onclick="thaubing_record_table.loadData(\''+data+'\'); thaubing_record_table.show(); thaubing_company_table.hide(); return false">'+data+'</button></td>';
                }
            }],
            buttons:[{
                text: "<i class='glyphicon glyphicon-menu-left'></i>回上頁" ,
                action: function (e, dt, node, config) {
                    thaubing_company_table.hide();
                    thaubing_group_table.show();
                }
            }]
        })    
    },      

    'loadData': function (data) {
        this.table_element.DataTable().clear();
        this.table_element.DataTable().rows.add(this.companyItems[data]).draw();
    },  

    'show': function(){
       $('#thaubing_company_area').css('display','inline-block');
    },

    'hide': function(){
        $('#thaubing_company_area').css('display','none');
    }
}

var thaubing_record_table={
    'fineRecordItems': {},
    'table_element': $('#thaubing_record'),

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "facility_name"},
                {data: "penalty_date"},
                {data: "penalty_money"},
                {data: "transgress_law"},
                {data: "is_petition"},
                {data: "petition_result"},
            ],
            order: [[1, 'desc']],
            dom: 'Bfrtlip',
            columnDefs: [],
            buttons:[{
                text: "<i class='glyphicon glyphicon-menu-left'></i>回上頁" ,
                action: function (e, dt, node, config) {
                    thaubing_record_table.hide();
                    thaubing_company_table.show();
                }
            }]
        })    
    },      

    'loadData': function (data) {
        this.table_element.DataTable().clear();
        this.table_element.DataTable().rows.add(this.fineRecordItems[data]).draw();
    },  

    'show': function(){
       $('#thaubing_record_area').css('display','inline-block');
    },

    'hide': function(){
        $('#thaubing_record_area').css('display','none');
    }
}

var taxdiscount_group_table={
    'groupItems':[],

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "group_no"},
                {data: "group_name_list"},
                {data: "has_discount"},
                {data: "has_fine_record"}
            ],
            order: [[2, 'desc']],
            dom: 'Bfrtlip',
            columnDefs: [{
                'targets': 0,
                'searchable': true,
                'orderable': true,
                'width': '1%',
                'render': function (data, type, full, meta) {
                    return '<td ><button class="btn btn-link" onclick="taxdiscount_company_table.loadData(\''+data+'\'); taxdiscount_company_table.show(); taxdiscount_group_table.hide(); return false">'+data+'</button></td>';
                }
            }],
            buttons:[]
        })    
    },        

    'loadData': function (table, data) {
        table.DataTable().clear();
        table.DataTable().rows.add(data).draw();
    },

    'show': function () {
       $('#taxdiscount_group_area').css('display','inline-block');
    },

    'hide': function(){
        $('#taxdiscount_group_area').css('display','none');
    }
}

var taxdiscount_company_table={
    'companyItems': {},
    'table_element': $('#taxdiscount_company'),

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "taxcode"},
                {data: "company_name"},
                {data: "taxdiscount"},
                {data: "has_fine_record"}
            ],
            order: [[2, 'desc']],
            dom: 'Bfrtlip',
            columnDefs: [
            ],
            buttons:[{
                text: "<i class='glyphicon glyphicon-menu-left'></i>回上頁" ,
                action: function (e, dt, node, config) {
                    taxdiscount_company_table.hide();
                    taxdiscount_group_table.show();
                }
            }]
        })    
    },      

    'loadData': function (data) {
        this.table_element.DataTable().clear();
        this.table_element.DataTable().rows.add(this.companyItems[data]).draw();
    },  

    'show': function(){
       $('#taxdiscount_company_area').css('display','inline-block');
    },

    'hide': function(){
        $('#taxdiscount_company_area').css('display','none');
    }
}