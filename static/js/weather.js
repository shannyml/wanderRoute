'use strict';

const getWeather = document.querySelector("#input-destination")

getWeather.addEventListener("submit", (evt) => {
    evt.preventDefault();

    const userInput = document.querySelector("#user-destination").value

    fetch(`get-weather?user-destination=${userInput}`)
    .then((response) => {
        return response.json()
    })
    .then((json) => {
        weatherForecast(json)
        // console.log(json)
    })
})

function weatherForecast(json) {

    const userInput = document.querySelector("#user-destination").value
    var forecastList = document.getElementsByClassName("forecast-results")[0]

    let results = json
    // console.log(results)
    let place = results.locations
    let forecast = place[`${userInput}`]['values']
    
    forecast.forEach(day => {
        console.log(day)
        let temp = day.temp
        let minTemp = day.mint
        let maxTemp = day.maxt
        let condition = day.conditions
        let dateTime = day.datetimeStr
        let date = dateTime.split("T")[0]

    const getForecast = document.createElement('tr')
    getForecast.innerHTML = `<td>${date}</td>
                            <td>${temp}°F</td>
                            <td>${condition}</td>
                            <td>${minTemp}°F</td>
                            <td>${maxTemp}°F</td>`
    forecastList.appendChild(getForecast)

    })
}