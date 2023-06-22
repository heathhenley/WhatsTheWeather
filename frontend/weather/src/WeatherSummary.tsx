import React, { useState, useEffect } from 'react';
import { useLoaderData } from 'react-router-dom'
import Card from 'react-bootstrap/Card'
import Loading from './Loading';
import './App.css'

export interface WeatherSummaryResults {
  zipcode: string;
  summarized_weather: string;
  role: string;
  location: string;
  icon_url: string;
  detail_url: string;
}

const WeatherCard = (props: WeatherSummaryResults) => {
  return (
    <>
      <div className="cardWrapper">
        <div className="cardBody">
          <div className="cardHeader">
            <div className="cardHeaderTitleWrap">
              <h2>{props.location}</h2>
              <div className="cardSubtitle mt-0 text-muted">
                {props.zipcode}
              </div>
            </div>
            <div className="cardHeaderImage">
              <img  src={props.icon_url} />
            </div>
          </div>
        </div>
        <div className="cardText">
          {props.summarized_weather.split('\n').map((line, index) => (
            <p key={index}>{line}</p>
          ))}
        </div>
        <div className="cardFooter">
          <div className="cardFooterItem">
            <a href={props.detail_url}
               target="_blank" rel="noopener">
                Detailed {props.zipcode} Weather
            </a>
          </div>
          <div className="cardFooterItem">
            <a href="https://www.weatherapi.com/"
               title="Free Weather API"
               target="_blank" rel="noopener">
              <img src='//cdn.weatherapi.com/v4/images/weatherapi_logo.png' alt="Weather data by WeatherAPI.com" />
              </a>
          </div>
        </div>
      </div>
    </>
  )
}

export const WeatherSummary = () =>  {
  const weatherInfo = useLoaderData() as WeatherSummaryResults;

  return (
    <div className="weatherSummaryContainer">
      <div className="weatherSummary">
        <WeatherCard {...weatherInfo} />
      </div>
    </div>
  )
}
