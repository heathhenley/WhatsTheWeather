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
          {props.summarized_weather}
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
