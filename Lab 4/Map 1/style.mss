Map {
  background-color: #b8dee6;
}

#countries {
  ::outline {
    line-color: #85c5d3;
    line-width: 2;
    line-join: round;
  }
  polygon-fill: #fff;
}


#earthquakes {
  [mag >= 1.0] { marker-width:3; }
  [mag >= 2.5] { marker-width:4; }
  [mag >= 4.5] { marker-width:5; }
  [mag >= 7.0] { marker-width:6; }
  marker-fill:#f45;
  marker-line-color:#813;
  marker-allow-overlap:true;
}
