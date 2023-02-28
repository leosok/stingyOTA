import os
import hashlib
try:
    import urequests as requests
except ImportError:
    print("No urequests found. Please provide your own library.")

class StingyOTA:
    """
    StingyOTA: A class to check for changes in a github repository and download only the changed files.

    !! Needs to be inizialized after internet connection is established !!

    Usage:
    from stingyota import StingyOTA
    stingyota = StingyOTA(branch, subfolder, requests_lib, version_file)
    if stingyota.has_new_version():
        stingyota.update()

    """
    def __init__(
        self, 
        user = 'leosok',
        repo = 'erika-esp32',
        branch = 'develop',
        subfolder = None,
        requests_lib = requests, # type: ignore
        version_file = '.version'
        ):
        """
        branch (str): The branch to check for updates
        subfolder (str): The subfolder to check for updates
        requests_lib (library): The requests library to use. Has to have a "get" method.
        version_file: The file to store the last hash in. Default is ".version"
        """

        self.requests_lib = requests_lib # type: ignore
        self.version_file = version_file
        self.remote_version = None
        self.subfolder = subfolder
        self.url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}"

    def _get_all_local_files(self, root = "/", ignore_hidden_dirs = True):
        """
        Recursive function to get all files in a folder.
        Returns a list of all files, whith the path relative to the folder.
        """
        files = []
        for item in os.listdir(root):
            item_path = os.path.join(root, item)
            print(item_path)
            if os.path.isfile(item_path):
                files.append(item_path)
                print("file: " + item_path)
            elif os.path.isdir(item_path):
                if ignore_hidden_dirs and not item.startswith('.'):
                    #print("DIR: " + item_path)
                    files += [os.path.join(item_path, f) for f in os.listdir(item_path)]
                else:
                    print("Hidden DIR: " + item_path)
            else:
                print("Unknown: " + item_path)
                #os.chdir('..')
        return files

    def _get_local_files_with_hash(self, root = "/", ignore_hidden_dirs = True):
        """
        Returns a dict of all files with the hash as value.
        """
        files = self._get_all_local_files(root)
        files_with_hash = {}
        for file in files:
            try:
                with open(file, 'rb') as f:
                    files_with_hash[file] = hashlib.sha256(f.read()).hexdigest()
            except OSError:
                pass
        return files_with_hash
        

    def _get_tree(self, url = None):
        if not url:
            url = self.url
        tree_json = self.requests_lib.get(url).json()
        return tree_json
    
    def _get_local_hash(self):
        try:
            with open(self.version_file, 'r') as f:
                return f.read()
        except FileNotFoundError:
            print("StingyOTA: No local version file found, so update will be started.")
            return False

    def has_new_version(self):
        tree_json = self._get_tree()
        if tree_json['sha'] == self._get_local_hash():
            return False
        else:
            return True

    def _update_local_version(self):
        if self.remote_version:
            with open(self.version_file, 'w') as f:
                f.write(self.remote_version)

    def _download_files(self):
        tree_json = self._get_tree()
        if self.subfolder:
            try:
                subfolder_json_url = [item_path for item_path in tree_json['tree'] if item_path['path'].startswith(subfolder)]
                subfolder_json_url = subfolder_json_url[0]['url']
                subfolder_json_url += "?recursive=1" # adding recursive to get all files in one request
            except IndexError:
                print(f"StingyOTA: Subfolder {self.subfolder} not found. Please check spelling.")
                raise
            sub_tree_json = self._get_tree(subfolder_json_url)
            #print(sub_tree_json)

            files = [item_path for item_path in sub_tree_json['tree'] if item_path['type'] == 'blob']
            print(f"StingyOTA: {len(files)} files found.")


    def update(self):
        """
        Checks for new version and downloads the files on restart if there is a new version.
        """
        if self.has_new_version():
            print("StingyOTA: New version found. Downloading files.")
            self._download_files()
            self._update_local_version()
        else:
            print("StingyOTA: No new version found.")