import React from "react";
import './Bar.css'

export const Bar = ({ data }) => {
    return (
        <div className="BarChart">
            // This is where we map through our data to create 
            // the different stacks of the bar chart, 
            // injecting the height and color via inline styling
            {data &&
                data.map((d) => {
                    return (
                        <div className="BarData" style={{ background: `${d.color}`, height: `${d.percent}%` }}>
                            <p className="PercentText">{d.percent + '%'}</p>
                        </div>
                    );
                })}
        </div>
    );
};

