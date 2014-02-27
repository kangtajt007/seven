// JavaScript Document
var play_mode = "order"; //取值：order: 顺序播放, single: 单曲播放, rand: 随机播放
var loop_mode = "list"; //取值: list: 列表循环, single: 单曲循环, none: 不循环
var oldCurPoint = 0,
    threshold = 0.1;
$(document.body).ready(function () {
    $.jPlayer.timeFormat.showHour = true;

    $("table.player_list_table>tbody").delegate('tr', 'mouseover mouseleave', function (e) {
        var me = $(this),
                div = $("div.more_func_div", me);
        if (e.type == 'mouseover') {
            div.removeClass('hidden');
        } else {
            div.addClass('hidden');
        }
    });
    $("table.player_list_table>tbody").delegate("a.play_musci", "click", function(){
        var tr = $(this).parents("tr");
        playMusic(tr);
    });

    $("#player").jPlayer({
        ready: function (event) {
        },
        play: function (event) {
            $(".song-name").html(event.jPlayer.status.media.title);
            var id = event.jPlayer.status.media.id;
        },
        ended: function (event) {
            casePlayMode();
        },
        timeupdate: function (event) {
            var percent = (event.jPlayer.status.currentTime / event.jPlayer.status.duration) * 100;
            $(".seek-bar").css("width", percent + "%");
            $("#duration").html($.jPlayer.convertTime(event.jPlayer.status.duration));
            updateLrc(event.jPlayer.status.currentTime);
        },
        solution: 'html, flash',
        supplied: "m4a",
        swfPath: __ctx + "media/swf/Jplayer.swf",
        wmode: "window",
        loop: false,
        volume: 1,
        cssSelectorAncestor: "",
        cssSelector: {
            currentTime: "#playtime",
            duration: "#totaltime",
            seekBar: ".download-bar",
            playBar: ".seek-bar",
            play: ".play",
            pause: ".pause",
            mute: ".mute",
            unmute: ".unmute",
            volumeBar: "#volumn",
            volumeBarValue: ".volumn-bar"
        }
    });

    //绑定停止按钮
    $(".btn-stop").click(function () {
        $("#playing-state").html("播放停止");
        //$("#player").jPlayer("clearMedia");
        $("#player").jPlayer("stop");
        return false;
    });

    //绑定上一曲，下一曲事件
    $(".pre,.next").click(function () {
        casePlayMode($(this).hasClass("pre"));
        return false;
    });

    //绑定循环模式
    $(".controls span a").click(function () {
        $(".controls span a.order-mode").removeClass("order-mode-select");
        $(".controls span a.random-mode").removeClass("random-mode-select");
        $(".controls span a.single-mode").removeClass("single-mode-select");

        var current_classname = $(this).attr("class").split(" ")[0];
        $(this).addClass(current_classname + "-select");
        switch (current_classname) {
            case "order-mode":
            {
                play_mode = "order";
                loop_mode = "list"
                break;
            }
            case "single-mode":
            {
                play_mode = "single";
                loop_mode = "single"
                break;
            }
            case "random-mode":
            {
                play_mode = "rand";
                loop_mode = "list";
                break;
            }
        }
        return false;
    });
});

function casePlayMode(pre){
    $(".song-name").html("播放完毕");
    var tbody = $("table.player_list_table > tbody");
    if (play_mode == "single" && loop_mode == "single") {
        var tr = $("tr.active-tr",tbody);
        playMusic(tr);
    }
    else if (play_mode == "rand") {
        var trAry = $("tr",tbody),
             max = trAry.length,
             targetIndex = GetRandomNum(0, max);
        trAry.each(function(){
            var me = $(this),
                myIndex = me.index();
            if(myIndex==targetIndex){
                playMusic(me);
                return false;
            }
        });
    }
    else{
        var tr = $("tr.active-tr",tbody),
             next = tr.next();
        if(pre){
            next = tr.prev();
        }
        if(!next||next.length==0){
            next = $("tr:first",tbody);
            if(pre){
                next = $("tr:last",tbody);
            }
        }
        playMusic(next);
    }
};

function playMusic(tr) {
    oldCurPoint = 0;
    $("ul.lrc-ul").empty();
    var activeTr = $("tr.active-tr");
    activeTr.removeClass("active-tr");
    activeTr.removeClass("info");
    $("td:first",tr).append($("#beating-elves"));
    tr.addClass("active-tr");
    tr.addClass("info");

    var songName = $("td.song-td",tr).text(),
        songId = $("input[songId]", tr).attr("songId"),
        albumPic = $("input[name='albumPic']",tr).val(),
        straUrl = $("input[name='songUrl']",tr).val(),
        albumName = $("input[name='album']",tr).val();

    if(!albumName||albumName=='undefined'){
        albumName = songName;
    }
    $("#ablum-span").text(albumName);
     if(!albumPic||albumPic=='undefined'){
        albumPic = __ctx + 'img/default_ablum_pic.jpg';
    }
    $("#ablum-img").attr("src",albumPic);
    if(straUrl&&straUrl!="undefined"){
        $("#player").jPlayer("setMedia", {title: songName, m4a: straUrl, id: songId}).jPlayer("play");
        var lrcUrl = $("input[name='lrcUrl']",tr).val();
        if(lrcUrl&&lrcUrl!="undefined"){
            $.get(lrcUrl,function(d){
                if(!d)return;
                initLrc(d);
            });
        }
    }
    else{
        if (!songId)return;
        var url = "/music/song/" + songId;
        $.get(url, function (d) {
            var obj = $.parseJSON(d),
                sonObj = obj.data.songList[0],
                songUrl = sonObj.songLink,
                lrcLink = sonObj.lrcLink;
            songUrl = songUrl.replace(/\?/g, "&63;").replace(/\//g, "&47;").replace(/\:/g, "&58;");
            songUrl = '/music/song/data/?path=' + songUrl;
            $("#player").jPlayer("setMedia", {title: sonObj.songName, m4a: songUrl, id: songId}).jPlayer("play");

            if(!lrcLink)return;
            $.get('/music/lrc'+lrcLink,function(d){
                if(!d)return;
                initLrc(d);
            });
        });
    }
};

function convertNum(point){
    var myregexp = /^\[(\d{2}):(\d{2})\.(\d{2})\]$/;
    var match = myregexp.exec(point),
        total = 0;
    if (match != null) {
        var min = match[1],
            second = match[2],
            millSecond = match[3];

        min = Number(min);
        second = Number(second);
        millSecond = Number(millSecond);
        total = min*60+second+millSecond/100;
    }
    return total;
};

function serialLrc(ary){
    var ul = $("ul.lrc-ul").empty();
    var size = ary.length;
    for(var i= 0;i<size;i++){
        var c = ary[i];
        var li = $('<li></li>').attr("point",c.point).text(c.word);
        if(!c.word){
            li.css("height","20px");
        }
        ul.append(li);
    }
};

function sortFunc(a,b){
    var x = Number(a.point),
        y = Number(b.point);
    return x==y?0:(x>y?1:-1);
};

function initLrc(d){
    var ary = d.split('\n'),
        lrcWordAry = [];
    if(!ary||ary.length==0)return;
    var myregexp = /(\[\d{2}:\d{2}\.\d{2}\]*)([^[|\]]*)/g;
    var size = ary.length;
    for(var i= 0;i<size;i++){
        var txt = ary[i],
            match = null,
            word = null,
            pointAry = [];
        while ((match = myregexp.exec(txt))) {
            pointAry.push(match[1]);
            word = word?word : match[2];
        }
        for(var j=0,c;c=pointAry[j++];){
            lrcWordAry.push({"point":convertNum(c),"word":word});
        }
    }
    if(!lrcWordAry||lrcWordAry.length==0)return;
    lrcWordAry.sort(sortFunc);
    serialLrc(lrcWordAry);
};

function updateLrc(currPoint){
    if(!currPoint)return;
    currPoint = Number(currPoint);
    if(!currPoint||isNaN(currPoint))return;
    currPoint = Number(currPoint.toFixed(2));
    if(currPoint <= oldCurPoint)return;
    var temp = currPoint - oldCurPoint;
    if( temp < threshold)return;
    oldCurPoint = currPoint;
    var ul = $("ul.lrc-ul");
    if(!ul||ul.length==0)return;
    var curLi = $("li.lrc-li-current",ul),
        first = $("li:first",ul);

    if(curLi&&curLi.length>0){
        var next = curLi.next("li");
        if(!next||next.length==0){
            //curLi.removeClass("lrc-li-current");
            return;
        }
        var point = next.attr("point");
        while(!point){
            next = curLi.next("li");
        }
        if(point&&Number(point)<currPoint){
            curLi.removeClass("lrc-li-current");
            next.addClass("lrc-li-current");
            var top = next.position().top,
                 lrcDiv = $("#lrc-ul-div"),
                 divHeight = lrcDiv.height();
            lrcDiv.animate({scrollTop:top-divHeight/3},500);
        }
    }
    else{
        if(!first||first.length==0)return;
        while(!first.attr("point")){
            first = first.next("li");
        }
        if(Number(first.attr("point"))<currPoint){
            first.addClass("lrc-li-current");
        }
    }
};

function GetRandomNum(Min,Max)
{
    var Range = Max - Min;
    var Rand = Math.random();
    return(Min + Math.round(Rand * Range));
}