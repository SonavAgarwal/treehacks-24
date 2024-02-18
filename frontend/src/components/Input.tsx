import React from "react";
import './Input.css'
import { useState } from "react";

export const Input = () => {
    const [inputValue, setInputValue] = useState('');
    const [isValid, setIsValid] = useState(true); // Initially true, assuming no input yet

    const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        const { value } = event.target;
        setInputValue(value);

        // Regular expression for URL validation
        const urlRegex = /^(ftp|http|https):\/\/[^ "]+$/;
        setIsValid(urlRegex.test(value));
    };

    return (
        <div>
            <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                placeholder="Enter a valid link"
            />
            {!isValid && (
                <p style={{ color: 'red' }}>Please enter a valid link</p>
            )}
        </div>
    );
};