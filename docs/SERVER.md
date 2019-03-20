## Quicklinks Server
Quicklinks server is an optional script that runs alongside with quicklinks that allows you to control and manage Quicklinks from your browsers or any API gateway.

### Usage
To start Quicklinks Server, all you need to do is run the following:

```bash
ql --start-server
```

To turn off the server, run:

```bash
sudo ql --stop-server
```

We require sudo access so we can modify your dotfile on your root directory.


### Notes
The reason why we do not directly modify you local files from your browser is because this is a really big security hole that most browsers by default prevent you from doing.
And secondly, we don't want you to modify your browser's internal settings to allow for browser write access as that could leave you vulnerable to bad actors.
