import React from "react";
import {
  Card,
  CardHeader,
  Heading,
  CardBody,
  Button,
  TextInput,
} from "grommet";
import Dropdown from "./dropdown";

const InputForm = () => {
  const [songName, setSongName] = React.useState("");

  const updateSongName = (event) => {
    setSongName(event.target.value);
  };

  const dropdownData = {
    Speed: [
      { label: "fast", value: "fast" },
      { label: "medium", value: "medium" },
      { label: "slow", value: "slow" },
    ],
    Tone: [
      { label: "happy", value: "happy" },
      { label: "sad", value: "sad" },
    ],
    Volume: [
      { label: "loud", value: "loud" },
      { label: "medium", value: "medium" },
      { label: "quiet", value: "quiet" },
    ],
    Instrument: [
      { label: "piano", value: "piano" },
      { label: "electric piano", value: "electric piano" },
      { label: "bass", value: "bass" },
    ],
    Repeatability: [
      { label: "1", value: "1" },
      { label: "2", value: "2" },
      { label: "3", value: "3" },
      { label: "4", value: "4" },
      { label: "5", value: "5" },
      { label: "6", value: "6" },
      { label: "7", value: "7" },
      { label: "8", value: "8" },
      { label: "9", value: "9" },
      { label: "10", value: "10" },
    ],
    Structuredness: [
      { label: "1", value: "1" },
      { label: "2", value: "2" },
      { label: "3", value: "3" },
    ],
  };

  const [selected, setSelected] = React.useState({});

  const handleChange = (name) => (event) => {
    setSelected((prevSelected) => ({
      ...prevSelected,
      [name]: event.target.value,
    }));
  };

  function API_call() {
    const encodedSongName = encodeURIComponent(songName);
    const requestBody = { ...selected };

    fetch(`http://127.0.0.1:5000/get-song-file/?title=${encodedSongName}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => {
        if (!response.ok) throw new Error(response.statusText);
        return response.blob();
      })
      .then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = `${songName}.wav`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
      })
      .catch((error) => console.error(error));
  }

  return (
    <Card height="medium" width="medium" background="dark-3">
      <CardHeader margin="xsmall" alignSelf="center">
        <Heading level="3">Create Your First Song!</Heading>
      </CardHeader>
      <CardBody margin="small" overflow="auto">
        <TextInput
          placeholder="Enter a song name..."
          value={songName}
          onChange={updateSongName}
        />
        <>
          {Object.entries(dropdownData).map(([name, options]) => (
            <div key={name}>
              <Dropdown
                title={name}
                name={name}
                options={options}
                onChange={handleChange(name)}
              />
            </div>
          ))}
        </>
        <Button primary margin="small" label="Go!" onClick={API_call} />
      </CardBody>
    </Card>
  );
};

export default InputForm;
