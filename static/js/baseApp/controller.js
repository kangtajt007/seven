'use strict';
var baseApp = angular.module('baseApp',[]).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('${');
    $interpolateProvider.endSymbol('}');
});

baseApp.controller('WeatherCtrl',['$scope',function($scope){
    $scope.getWeatherInfo = function(){
        $.base64.utf8encode = true;
        var remoteCityWeatherBase64 = $.cookie("remote_city_weather"),
            remote_ip_info = remote_ip_info||null,
            jsonStr;
        if(!remoteCityWeatherBase64 && remote_ip_info){
            var cityName = remote_ip_info["city"];
            if(cityName){
                var url = '/utente/cityName/' + cityName + '/';
                $.get(url,function(d){
                    if(d){
                        jsonStr = d;
                    }
                });
            }
        }
        else if(remoteCityWeatherBase64){
            remoteCityWeatherBase64 = remoteCityWeatherBase64.replace(/\\012/g, "");
            jsonStr = $.base64.atob(remoteCityWeatherBase64,true);
        }
        if(jsonStr){
            jsonStr = $.parseJSON(jsonStr);
            if(jsonStr && jsonStr.weatherinfo){
                $scope.data = jsonStr.weatherinfo;
                return 'weather-div';
            }
        }
        else{
            $scope.data = {"img1":"n0.gif"};
        }
         return 'hidden';
    };
}]);

baseApp.filter('reverse', function () {
    return function (input, uppercase) {
        var out = "";
        for (var i = 0; i < input.length; i++) {
            out = input.charAt(i) + out;
        }
        if (uppercase) {
            out = out.toUpperCase();
        }
        return out;
    };
});

baseApp.controller('MusicCtrl', ['$scope','$http', function ($scope,$http) {
    $scope.list = [{"song_id":"1","song":"the fox","singer":"Ylvis","url":__ctx + "audio/123.mp3","lrc":__ctx + "lrc/thefox.lrc"}];
    $scope.search = function(music){
        if(!music.word)return;
        $http.get("/music/query/" + music.word).success(function(d){
            if(typeof d =="string")return;
            $scope.list = d;
        });
    };
}]);