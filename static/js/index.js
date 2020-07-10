$(document).ready(function(){
// 


// 课程数量-加载-面授
function loadCourse(){
  $.get('assistant?dp_search='+{{data|safe}}+' sub_ms',function(json,status){
    var sels = "";
    $.each(json.data, function (k, v) {
			sels += `<div class="layui-inline"><select lay-filter="course_ms" class="course_ms" name="city" lay-verify=""><option value="${v.course}">${v.course}</option></select></div>`;
    });
    sels += '<div class="layui-inline"><select lay-filter="course_ms" class="course_ms" name="city" lay-verify=""><option value="请选择">请选择</option></select></div>'
    $("#kechengxuanze_mianshou").html(sels);
  });
}


loadCourse();

$(".course_ms").eq(0).parents().eq(1).click(function(){
  $.get('assistant?dp_menu=course_ms', function (json) {
    var html = '';
    for (var i = 0; i < json.data.length; i++) {
      // console.log(json.data[i].s_name);
      html += '<option value="' + json.data[i].id + '">' + json.data[i].course
         + '</option>';
    };
    $('.course_ms').html(html)
  });
})



})