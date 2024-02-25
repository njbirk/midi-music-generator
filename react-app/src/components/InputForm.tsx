import React from "react";
import {
  Card,
  CardHeader,
  Heading,
  CardBody,
  Button,
  TextInput,
} from "grommet";

const InputForm = () => {
  const [songName, setSongName] = React.useState("");

  const updateSongName = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSongName(event.target.value);
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
        <Button primary margin="small" label="Go!" />
      </CardBody>
    </Card>
  );
};

export default InputForm;
