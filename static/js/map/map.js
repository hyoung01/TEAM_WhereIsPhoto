// 지도 초기 설정
var container = document.getElementById('map');
var options = {
    center: new kakao.maps.LatLng(37.557074, 126.929276), // 임의의 중심 좌표
    level: 4 // 확대 축소 정도
};

var map = new kakao.maps.Map(container, options); // 지도 생성


// 지도 가장자리 꾸미기 관련 ------------------------------------------------------
// 지도 확대 축소를 제어할 수 있는  줌 컨트롤을 생성합니다
var zoomControl = new kakao.maps.ZoomControl();
map.addControl(zoomControl, kakao.maps.ControlPosition.LEFT);

// 지도가 확대 또는 축소되면 마지막 파라미터로 넘어온 함수를 호출하도록 이벤트를 등록합니다
kakao.maps.event.addListener(map, 'zoom_changed', function() {        
    
    // 지도의 현재 레벨을 얻어옵니다
    var level = map.getLevel();
    
    var message = '현재 지도 레벨은 ' + level + ' 입니다';
    var resultDiv = document.getElementById('result');  
    resultDiv.innerHTML = message;
    
});


// blue pin으로 된 marker image 생성
var imageSrc = '../static/icons/pin_blue.png'
var imageSize = new kakao.maps.Size(32, 32);
var markerImage = new kakao.maps.MarkerImage(imageSrc, imageSize); 


// 1 현재 위치 찍기 -----------------------------------------------------------------------------

// 현재 위치 차단 확인하는 코드  https://kjwan4435.tistory.com/66
var gps_use = null; //gps의 사용가능 여부
var gps_lat = null; // 위도
var gps_lng = null; // 경도
var gps_position; // gps 위치 객체

gps_check();
// gps가 이용가능한지 체크하는 함수이며, 이용가능하다면 show location 함수를 불러온다.
// 만약 작동되지 않는다면 경고창을 띄우고, 에러가 있다면 errorHandler 함수를 불러온다.
// timeout을 통해 시간제한을 둔다.
function gps_check(){
    console.log("일단 이거 gps check 했고")

    if (navigator.geolocation) {
        console.log("이걸 안띄우?나?")
        var options = {timeout:60000};
        navigator.geolocation.getCurrentPosition(showLocation, errorHandler, options);
    } else {
        alert("GPS_추적이 불가합니다.");
        gps_use = false;
    }
}


// gps 이용 가능 시, 위도와 경도를 반환하는 showlocation함수.
function showLocation(position) {
    gps_use = true;
    gps_lat = position.coords.latitude;
    gps_lng = position.coords.longitude;
    console.log("Showlocation도 햇지?")

    var markerPosition  = new kakao.maps.LatLng(gps_lat,gps_lng); 
            
    var marker = new kakao.maps.Marker({  
        map: map, 
        position: markerPosition, 
        image: new kakao.maps.MarkerImage('../static/icons/pin_current.png', new kakao.maps.Size(24, 24))
    }); 

    marker.setMap(map);
    map.setCenter(markerPosition);      
    map.setLevel(7)
}


// error발생 시 에러의 종류를 알려주는 함수.
function errorHandler(error) {
    if(error.code == 1) {
        alert("위치 엑세스가 거부되었습니다.\n기본 위치로 이동합니다.");
    } else if( err.code == 2) {
        alert("위치를 반환할 수 없습니다.");
    }
    gps_use = false;
}



// 2 부스 위치 찍기 -----------------------------

// 주소 정보 가져오기
// 주소-좌표 변환 객체를 생성합니다
var geocoder = new kakao.maps.services.Geocoder();

var callback = function(result, status) {
    console.log(status)
    // 정상적으로 검색이 완료됐으면 
    if (status === kakao.maps.services.Status.OK) {

        var coords = new kakao.maps.LatLng(result[0].y, result[0].x);

        // 결과값으로 받은 위치를 마커로 표시합니다
        var marker = new kakao.maps.Marker({
            map: map,
            position: coords,
            image: markerImage
        });
        marker.setMap(map);

    }
    else {
        console.log("안돼?")
        console.log(result)
    }
};

// 주소로 좌표를 검색합니다
var boothList = document.getElementById('accordionList');
let total = boothList.childElementCount; // count todos    

    for (let i=0; i<total; i++) {
        
        const element = document.getElementById(`mapdetail-${i}`);
        let address = element.children[1].innerHTML
        // console.log(typeof address)
        if (address == "인천 미추홀구 숙골로87번길 5 5블럭 1층 40호") {
            console.log("yes")
            address = "인천 미추홀구 숙골로87번길 5";
        }
        geocoder.addressSearch(address, callback);

    }