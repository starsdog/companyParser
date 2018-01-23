var year=2016;
function open_graph(year, group_name){
    window.open('/companydata/graph.html?year='+year+'&group='+group_name, '關係圖', config='height=800,width=1024');
}
var groupName_table={
    'group_map':new Object(),

    'prepareTable':function(result){
        var row='<tr>';
        var count=1;
        $.each(result, function (index, group_no) {
            var link='/group/name/'+group_no;
            row+='<td><a href="'+link+'">'+groupName_table.group_map[group_no]+'</td>';
            if((count%5)==0){
                row+='</tr><tr>';
            }
            count+=1;
        });  
        row += '</tr>'; 
        $('#table_group_list').append(row); 
    },

    'loadData':function(result){
        if(Object.keys(groupName_table.group_map)!=0){
            groupName_table.prepareTable(result);
        }
        else{
            group_file='/companydata/group_relation/groupName_'+year+'.json';
            $.get(group_file,function(data){
                groupName_table.group_map=data;
                groupName_table.prepareTable(result);
            });

        }
    },

    'show':function(){
        $('#table_group_list_area').css('display','inline-block');
    },

    'hide': function(){
        $('#table_group_list_area').css('display','none');
    }
}
var summery_table={
    'loadData': function (data) {
       /*
       var row='<tr><td>'+data.group_name+'</td><td>'+data.company_amount+'</td><td>'+data.has_fine;
       row+='</td><td>'+data.fine_company_amount+'</td><td>'+data.fine_record_num+'</td><td>'+data.fine_penalty_amount;
       row+='</td><td><button class="btn btn-link" onclick="open_graph(); return false;"><i class="glyphicon glyphicon-stats"></i></button></tr>';
       $('#table_summery').append(row);
       */
       var row='<div><h1>'+data.group_name+'</h1></div>';
       row+='<div><span>集團公司總數: '+data.company_amount+'</span></div>';
       if (data.has_fine==true)
            row+='<div><span>是否有裁罰記錄: 是</span></div>';
       else
            row+='<div><span>是否有裁罰記錄: 否</span></div>';
       row+='<div><span>有裁罰記錄公司總數: '+data.fine_company_amount+'</span></div>';
       row+='<div><span>裁罰記錄總數: '+data.fine_record_num+'</span></div>';
       row+='<div><span>裁罰金額總數: '+data.fine_penalty_amount+'</span></div>';
       row+='<div><span>關係圖: </span><button class="btn btn-link" onclick="open_graph(\''+year+'\',\''+data.group_no+'\'); return false;"><i class="glyphicon glyphicon-stats"></i></button></div>';
       $('#summery_content').append(row);
    },  

    'show': function(){
       $('#table_summery_area').css('display','inline-block');
    },

    'hide': function(){
        $('#table_summery_area').css('display','none');
    }

}

var fine_company_table={
    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "name"},
                {data: "taxcode"},
                {data: "fine_num"},
                {data: "penalty_amount"},
            ],
            order: [[1, 'desc']],
            dom: 'Bfrtlip',
            columnDefs: [{
                'targets': 1,
                'searchable': true,
                'orderable': true,
                'width': '1%',
                'render': function (data, type, full, meta) {
                    return '<td ><button class="btn btn-link" onclick="query_fine_record(\''+data+'\'); return false">'+data+'</button></td>';
                }
            }],
            buttons:[]
        })    
    },      

    'loadData': function (table, data) {
        table.DataTable().clear();
        table.DataTable().rows.add(data).draw();
    },  

    'show': function(){
       $('#table_fine_company_area').css('display','inline-block');
    },

    'hide': function(){
        $('#table_fine_company_area').css('display','none');
    }

}

var fine_record_table={
    'fineItems': {},
    
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
                text: "<i class='glyphicon glyphicon-menu-left'></i>回裁罰總表" ,
                action: function (e, dt, node, config) {
                    fine_record_table.hide();
                    fine_company_table.show();
                }
            }]
        })    
    },      

    'loadData': function (table, data) {
        table.DataTable().clear();
        table.DataTable().rows.add(data).draw();
    },  

    'show': function(){
       $('#table_fine_record_area').css('display','inline-block');
    },

    'hide': function(){
        $('#table_fine_record_area').css('display','none');
    }
}

var company_table={
    'companyItems': {},
    'table_element': $('#table_company'),
    'group_name':'',
    'year':2013,

    'init': function (table) {
        var _table = table.DataTable({
            autoWidth: false,
            columns: [
                {data: "taxcode"},
                {data: "name"},
                {data: "source_list"}
            ],
            order: [[0, 'asc']],
            dom: 'Bfrtlip',
            columnDefs: [],
            buttons:[]
        })    
    },      

    'loadData': function (table, data) {
        table.DataTable().clear();
        table.DataTable().rows.add(data).draw();
    },  

    'show': function(){
       $('#table_company_area').css('display','inline-block');
    },

    'hide': function(){
        $('#table_company_area').css('display','none');
    }
}

var table = $("#table_company");
company_table.init(table);
var table = $("#table_fine_record");
fine_record_table.init(table);
var table = $("#table_fine_company");
fine_company_table.init(table);
$('#search_warning').css('display','none');



