'use strict';

// get recommendation, show list of recommendations, add reach recommendations to
// itinerary list
let itineraryItems = []

const getRecommendations = document.querySelector('#get-recommendations')

getRecommendations.addEventListener("click", (evt) => {
    evt.preventDefault();

    const user_input_location = document.querySelector('#interested-destination').value
    const user_input_type = document.querySelector('#location-type').value

    

    fetch(`/get-recommendations?interested-destination=${user_input_location}+location-type=${user_input_type}`)
    .then((response) => {
        return response.json()
    })
    .then((json) => {
        updateDom(json.data)
        initMap(json)
    }
    )
})

function updateDom(json) {
    let listOfBusiness = json.results
    var resultList = document.getElementsByClassName("location-results")[0]

    // clear list every time
    while (resultList.firstChild) {
        resultList.removeChild(resultList.firstChild)
    }

    // set new list items
    listOfBusiness.forEach(business => {
        let businessName = business.name
        let businessAddress = business.vicinity
        let place_id = business.place_id
        let lat = business.geometry.location.lat
        let lng = business.geometry.location.lng

        const clickToAdd = document.createElement('li')
        clickToAdd.innerHTML = `<button data-locationname="${businessName}" data-placeid="${place_id}" data-lat="${lat}" data-lng="${lng}" onclick="addToList(this)" id="recommendation-bt">Add</button><span>  ${businessName}</span>`
        clickToAdd.classList.add("py-1")
        //clickToAdd.innerHTML = '<button data-locationname="'+businessName+'"data-placeid="'+ place_id +'" data-lat="'+ lat +'" data-lng="'+ lng +'" onClick = "addToList(this)">' +'Location: ' + businessName + ' Address: ' + businessAddress +"</button>"
        resultList.appendChild(clickToAdd)
    })
}

function addToList(obj) {
    const name = obj.dataset.locationname
    const currentList = document.querySelector("#itinerary-list")
    const itineraryListItem = document.createElement('li')
    const itineraryInput = document.createElement('input')
    itineraryListItem.innerHTML = `${name} <img src="/static/images/trash.png" width="20px">`
    itineraryListItem.addEventListener('click', function() {
        this.parentNode.removeChild(this);
        })
    currentList.appendChild(itineraryListItem)
    currentList.appendChild(itineraryInput)
    itineraryInput.name = "itinerary-list"
    itineraryInput.type = "hidden"
    itineraryInput.value = obj.dataset.placeid

    const itineraryInfo = {'place_id': obj.dataset.placeid, 'lat': obj.dataset.lat, 'lng':obj.dataset.lng, 'location_name':obj.dataset.locationname}
    itineraryItems.push(itineraryInfo)
    console.log(`add item push list------ ${itineraryItems}`)
    console.log(itineraryItems)
}

console.log(`gloabal final list(appended?)------ ${itineraryItems}`)
console.log(itineraryItems)
const submitForm = document.querySelector('#submit-btn')
submitForm.addEventListener('click', (evt) => {
    evt.preventDefault()
    submitItinerary()
})


function submitItinerary() {

    let itinerary_id = document.querySelector("#itinerary-id").value
    let user_id = document.querySelector("#user-id").value

    const dataRequest = {itineraryId: itinerary_id, itineraryItems: itineraryItems}


    fetch('/get-itinerary-info', {
        method: 'POST',
        credentials: 'include', //send along the cookies as well
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dataRequest), // change to itineraryItems
        cache: 'default'
    })
    .then((response) => {
        console.log(response.status)
        response.status
        // return response.json()
    })
    .then((data) => {
        // fix this
        window.location.href=`/profile/${user_id}`
    });
}

function initMap(json) {
    if (json == undefined) {
        const basicMap = new google.maps.Map(document.querySelector('#map'), {
            center: {lat: 34.0195, lng:-118.4912},
            zoom: 4
        });
    }

    else {
    let coordinates = json['coordinates']
    const userInput = document.querySelector('#interested-destination').value
  
    const locationCoord = {
        lat: coordinates['lat'],
        lng: coordinates['lng']
    }
    const basicMap = new google.maps.Map(document.querySelector('#map'), {
        center: locationCoord,
        zoom: 13
    });
  
    const locationMarker = new google.maps.Marker({
        position: locationCoord,
        title: "LA",
        map: basicMap,
    });

    const locationInfo = new google.maps.InfoWindow({
        content: `<h1>${userInput}</h1>`,
    });

    locationInfo.open(basicMap, locationMarker);

    let locationList = json['data']['results']
    const markers = [];
    
    for (const location of locationList) {
        let coords = {lat: location['geometry']['location']['lat'], lng: location['geometry']['location']['lng']}
        let name = location['name']
        let address = location['vicinity']
    
        markers.push(
            new google.maps.Marker({
            position: coords,
            title: name,
            address: address,
            map: basicMap
            })
        )
    }

    for (const marker of markers) {
        const markerInfo = `
        <h1>${marker.title}</h1>
        <p> Address: ${marker.address}</p>
        `;

        const infoWindow = new google.maps.InfoWindow({
            content: markerInfo,
            maxWidth: 200,
        });
    
        marker.addListener('click', () =>{
            infoWindow.open(basicMap, marker);
        })
        marker.setMap(basicMap)
        
    }}
}

initMap()