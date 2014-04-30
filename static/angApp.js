
var angApp = angular.module('angApp', []);
 
angApp.controller('uploadCtrl', function ($scope, $http) {

	$scope.upFile = null;
	$scope.version = null;
	
	$scope.setFile = function (element) {        
		$scope.upFile = element.files[0];
    }
	
	$scope.xl_data = {}
	$scope.sendFile = function(theFile){
		formData = new FormData()
		formData.append("upFile",$scope.upFile)
		formData.append("version",$scope.version)
		var url = "/api/upload/"+$scope.version
		$http.post(url, formData, {
			headers: { 'Content-Type': undefined },
			transformRequest: angular.identity
			}).success(function(resp){
				console.log(resp)
				$scope.xl_data = resp
			});
		}	
});

angApp.controller('downloadableCtrl', function ($scope, $http) {


	$scope.downloadables = null
	$scope.get_downloadables = function() {
		$http.get("/api/downloadables").success(function(resp){
			console.log(resp)
			$scope.downloadables = resp.forms
			$scope.upload_response = "This will be a success or error message... depending"
		})
	}

	$scope.get_download = function(path){
		$http.get("/api/download/"+path).success(function(resp){

		})
	}


});
