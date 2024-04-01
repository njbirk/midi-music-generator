import React from "react";
import {
  Card,
  CardHeader,
  Heading,
  CardBody,
  Button,
  TextInput,
} from "grommet";
import Dropdown from './dropdown'

const InputForm = () => {
  const [songName, setSongName] = React.useState("");

  const updateSongName = (event) => {
    setSongName(event.target.value);
  };

  function API_call() {
    const encodedSongName = encodeURIComponent(songName);
    fetch(`http://127.0.0.1:5000/get-song-file/?title=${encodedSongName}`, {
      method: "POST",
      // Other settings like 'credentials' go here if needed
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


  const dropdownData = {
    dropdownOne: [
      { label: 'Option 1', value: 'option1' },
      { label: 'Option 2', value: 'option2' },
    ],
    dropdownTwo: [
      { label: 'Option A', value: 'optionA' },
      { label: 'Option B', value: 'optionB' },
    ],
  };

  const [selected, setSelected] = React.useState({});


  const handleChange = (name) => (event) => {
    setSelected(prevSelected => ({
      ...prevSelected,
      [name]: event.target.value,
    }));
  };


  return (
    <Card height="medium" width="medium" background="dark-3">
      <CardHeader margin="xsmall" alignSelf="center">
        <Heading level="3">Create Your First Song!</Heading>
      </CardHeader>
      <CardBody margin="small">
        <TextInput
          placeholder="Enter a song name..."
          value={songName}
          onChange={updateSongName}
        />
        <>
        {Object.entries(dropdownData).map(([name, options]) => (
        <div key={name}>
          <Dropdown
            name={name}
            options={options}
            onChange={handleChange(name)}
          />
        </div>))}
        </>
        <Button primary margin="small" label="Go!" onClick={API_call} />
      </CardBody>
    </Card>
  );
};

export default InputForm;
