import subprocess, os, textwrap

@click.command()
@click.argument(
    'path_to_repo',
    type = click.Path(
        exists = True, dir_okay = True, file_okay = False, writable = True),
    help = "path to the github repo to initialize")
def setup_config(path_to_repo):
    os.chdir(path_to_repo)
    configure_git = subprocess.run(['git', 'config', '--local', 'diff.bencode.textconv=cat_bencode'], check = True)

    with open(".gitattributes", "a+") as f:
        f.write(textwrap.dedent(
        """
        # Treat the following files as `bencode`
        *.torrent diff=bencode
        *.fastresume diff=bencode
        """))
