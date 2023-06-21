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
      <Card>
      <Card.Body>
        <Card.Title>
          <div className="cardHeader">
            {props.location}
            <img  src={props.icon_url} />
            </div>
        </Card.Title>
        <Card.Subtitle
          className="mb-2 text-muted">
          {props.zipcode}
        </Card.Subtitle>
   
        <Card.Text>
          {props.summarized_weather}
        </Card.Text>
      </Card.Body>
    </Card>
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
