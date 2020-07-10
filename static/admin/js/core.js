// Core javascript helper functions




// basic browser identification & version
var isOpera = (navigator.userAgent.indexOf("Opera") >= 0) && parseFloat(navigator.appVersion);
var isIE = ((document.all) && (!isOpera)) && parseFloat(navigator.appVersion.split("MSIE ")[1].split(";")[0]);

// quickElement(tagType, parentReference [, textInChildNode, attribute, attributeValue ...]);
function quickElement() {
    'use strict';
    var obj = document.createElement(arguments[0]);
    if (arguments[2]) {
        var textNode = document.createTextNode(arguments[2]);
        obj.appendChild(textNode);
    }
    var len = arguments.length;
    for (var i = 3; i < len; i += 2) {
        obj.setAttribute(arguments[i], arguments[i + 1]);
    }
    arguments[1].appendChild(obj);
    return obj;
}

// "a" is reference to an object
function removeChildren(a) {
    'use strict';
    while (a.hasChildNodes()) {
        a.removeChild(a.lastChild);
    }
}

// ----------------------------------------------------------------------------
// Find-position functions by PPK
// See https://www.quirksmode.org/js/findpos.html
// ----------------------------------------------------------------------------
function findPosX(obj) {
    'use strict';
    var curleft = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curleft += obj.offsetLeft - ((isOpera) ? 0 : obj.scrollLeft);
            obj = obj.offsetParent;
        }
        // IE offsetParent does not include the top-level
        if (isIE && obj.parentElement) {
            curleft += obj.offsetLeft - obj.scrollLeft;
        }
    } else if (obj.x) {
        curleft += obj.x;
    }
    return curleft;
}

function findPosY(obj) {
    'use strict';
    var curtop = 0;
    if (obj.offsetParent) {
        while (obj.offsetParent) {
            curtop += obj.offsetTop - ((isOpera) ? 0 : obj.scrollTop);
            obj = obj.offsetParent;
        }
        // IE offsetParent does not include the top-level
        if (isIE && obj.parentElement) {
            curtop += obj.offsetTop - obj.scrollTop;
        }
    } else if (obj.y) {
        curtop += obj.y;
    }
    return curtop;
}

//-----------------------------------------------------------------------------
// Date object extensions
// ----------------------------------------------------------------------------
(function () {
    'use strict';
    Date.prototype.getTwelveHours = function () {
        var hours = this.getHours();
        if (hours === 0) {
            return 12;
        } else {
            return hours <= 12 ? hours : hours - 12;
        }
    };

    Date.prototype.getTwoDigitMonth = function () {
        return (this.getMonth() < 9) ? '0' + (this.getMonth() + 1) : (this.getMonth() + 1);
    };

    Date.prototype.getTwoDigitDate = function () {
        return (this.getDate() < 10) ? '0' + this.getDate() : this.getDate();
    };

    Date.prototype.getTwoDigitTwelveHour = function () {
        return (this.getTwelveHours() < 10) ? '0' + this.getTwelveHours() : this.getTwelveHours();
    };

    Date.prototype.getTwoDigitHour = function () {
        return (this.getHours() < 10) ? '0' + this.getHours() : this.getHours();
    };

    Date.prototype.getTwoDigitMinute = function () {
        return (this.getMinutes() < 10) ? '0' + this.getMinutes() : this.getMinutes();
    };

    Date.prototype.getTwoDigitSecond = function () {
        return (this.getSeconds() < 10) ? '0' + this.getSeconds() : this.getSeconds();
    };

    Date.prototype.getHourMinute = function () {
        return this.getTwoDigitHour() + ':' + this.getTwoDigitMinute();
    };

    Date.prototype.getHourMinuteSecond = function () {
        return this.getTwoDigitHour() + ':' + this.getTwoDigitMinute() + ':' + this.getTwoDigitSecond();
    };

    Date.prototype.getFullMonthName = function () {
        return typeof window.CalendarNamespace === "undefined" ?
            this.getTwoDigitMonth() :
            window.CalendarNamespace.monthsOfYear[this.getMonth()];
    };

    Date.prototype.strftime = function (format) {
        var fields = {
            B: this.getFullMonthName(),
            c: this.toString(),
            d: this.getTwoDigitDate(),
            H: this.getTwoDigitHour(),
            I: this.getTwoDigitTwelveHour(),
            m: this.getTwoDigitMonth(),
            M: this.getTwoDigitMinute(),
            p: (this.getHours() >= 12) ? 'PM' : 'AM',
            S: this.getTwoDigitSecond(),
            w: '0' + this.getDay(),
            x: this.toLocaleDateString(),
            X: this.toLocaleTimeString(),
            y: ('' + this.getFullYear()).substr(2, 4),
            Y: '' + this.getFullYear(),
            '%': '%'
        };
        var result = '',
            i = 0;
        while (i < format.length) {
            if (format.charAt(i) === '%') {
                result = result + fields[format.charAt(i + 1)];
                ++i;
            } else {
                result = result + format.charAt(i);
            }
            ++i;
        }
        return result;
    };

    // ----------------------------------------------------------------------------
    // String object extensions
    // ----------------------------------------------------------------------------
    String.prototype.pad_left = function (pad_length, pad_string) {
        var new_string = this;
        for (var i = 0; new_string.length < pad_length; i++) {
            new_string = pad_string + new_string;
        }
        return new_string;
    };

    String.prototype.strptime = function (format) {
        var split_format = format.split(/[.\-/]/);
        var date = this.split(/[.\-/]/);
        var i = 0;
        var day, month, year;
        while (i < split_format.length) {
            switch (split_format[i]) {
                case "%d":
                    day = date[i];
                    break;
                case "%m":
                    month = date[i] - 1;
                    break;
                case "%Y":
                    year = date[i];
                    break;
                case "%y":
                    year = date[i];
                    break;
            }
            ++i;
        }
        // Create Date object from UTC since the parsed value is supposed to be
        // in UTC, not local time. Also, the calendar uses UTC functions for
        // date extraction.
        return new Date(Date.UTC(year, month, day));
    };

})();
// ----------------------------------------------------------------------------
// Get the computed style for and element
// ----------------------------------------------------------------------------
function getStyle(oElm, strCssRule) {
    'use strict';
    var strValue = "";
    if (document.defaultView && document.defaultView.getComputedStyle) {
        strValue = document.defaultView.getComputedStyle(oElm, "").getPropertyValue(strCssRule);
    } else if (oElm.currentStyle) {
        strCssRule = strCssRule.replace(/\-(\w)/g, function (strMatch, p1) {
            return p1.toUpperCase();
        });
        strValue = oElm.currentStyle[strCssRule];
    }
    return strValue;
}



//自定义
window.onload = function () {


    if (location.pathname == '/adminmoodle/moodleuser/') {
        //用户页面
        // document.getElementsByClassName('object-tools')[0].removeChild(document.getElementsByClassName('object-tools')[0].getElementsByTagName('li')[0])
        // let excel = document.createElement("a");
        // excel.href = '/v1/moodle/excel'
        // excel.id = 'excel_teacher'
        // excel.target = '_blank'

        // let excel_li = document.createElement("li");
        // excel_li.appendChild(excel);

        // let node = document.createTextNode("导入Excel分配课程(学生需在小程序中注册)");
        // excel.appendChild(node);

        // let element = document.getElementsByClassName('object-tools')[0];
        // element.appendChild(excel_li);

        prof_new = document.getElementsByClassName('object-tools')[0].getElementsByTagName('a')[0]
        prof_new.innerHTML = '创建单个用户(教授或学员)'

        search = document.getElementById('changelist-search').getElementsByTagName('input')[1]
        search.value = '搜索(邮箱/姓名)'

    } else if (location.pathname == '/adminmoodle/moodlecourse/') {
        //课程页面
        // creat_cou = document.getElementsByClassName('object-tools')[0].getElementsByTagName('li')[0]
        // document.getElementsByClassName('object-tools')[0].removeChild(creat_cou)
        search = document.getElementById('changelist-search').getElementsByTagName('input')[1]
        search.value = '搜索课程名称'

    } else if (location.pathname == '/adminmoodle/moodlecus/') {
        //CUS

        let excel = document.createElement("a");
        excel.href = '/v1/moodle/excel'
        excel.id = 'excel_teacher'
        excel.target = '_blank'

        let excel_li = document.createElement("li");
        excel_li.appendChild(excel);

        let node = document.createTextNode("导入Excel分配课程(学生需在小程序中注册)");
        excel.appendChild(node);

        let element = document.getElementsByClassName('object-tools')[0];
        element.appendChild(excel_li);


        search = document.getElementById('changelist-search').getElementsByTagName('input')[1]
        search.value = '搜索(姓名/课程名)'
    } else if (location.pathname == '/adminmoodle/moodlevideo/') {
        //Video
        search = document.getElementById('changelist-search').getElementsByTagName('input')[1]
        search.value = '搜索课程名称'
    } else if (location.pathname == '/adminmoodle/moodleexam/') {
        //考试表
        search = document.getElementById('changelist-search').getElementsByTagName('input')[1]
        search.value = '搜索(姓名/课程名)'
    } else if (location.pathname == '/adminmoodle/moodleexam/add/') {
        //考试表新增

        let sele = document.getElementsByTagName('select')

        document.getElementById('id_exam_subject').accept=".pdf"

        sele[2].onchange = function () {
            // console.log(sele[2].value)
            if (sele[2].value != 'online'){
                document.getElementById('id_exam_subject').accept="*"
            }else{
                document.getElementById('id_exam_subject').accept=".pdf"
            }
        }

        

        
        
        sele[0].onchange = function () {
            // console.log(sele[0].value)

            var xmlhttp;
            if (window.XMLHttpRequest) {
                //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
                xmlhttp = new XMLHttpRequest();
            } else {
                // IE6, IE5 浏览器执行代码
                xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
            }
            xmlhttp.onreadystatechange = function () {
                if (xmlhttp.readyState == 4 && xmlhttp.status == 200) {

                    let sele2_father = document.getElementsByClassName('related-widget-wrapper')[1]

                    sele2_father.removeChild(sele[1])

                    sele2_father.innerHTML = xmlhttp.responseText

                    // sele[1].removeChild(sele[1].getElementsByTagName('option'))
                    // sele[1].replaceChild(xmlhttp.responseText) 
                }
            }
            xmlhttp.open("GET", `/prof_course/${sele[0].value}`, true);
            xmlhttp.send();



        }
    }

    if (document.getElementsByClassName('object-tools').length != 0) {
        document.getElementsByClassName('object-tools')[0].getElementsByTagName('a')[0].target = '_blank'
    }


    let x = document.getElementsByTagName('tbody')
    for (var i = 0; i < x.length; i++) {
        // x[i].getElementsByTagName('a')[0].setAttribute('target','_blank')
        x[i].getElementsByTagName('a')[0].target = '_blank'
    }


}