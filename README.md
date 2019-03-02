# PythonRegistryDiffer
A simple registry diffing tool &amp; library written in Python.


        USAGE:

                new-database : Creates a new database to host images of the registry. Requires the use of -f or -m.

                new-image   : Creates a new comparison image. It will only check the HKEYs that the first image was 
                             created with. Note: You don't need to call this option to create the first image; new-db creates
                             a baseline image unless called with the -e option.

                list-images : Lists the number of current images in the db and some cursory details.

                diff-images : Generates a report that compares two different registry images. Enter the image numbers from 
                             list-images as arguments to designate which images to compare. Use "-f filename" to save the report
                             to a file. Examples:
                            "PythonRegistryDiffer> diff-images 0 3" 
                            "PythonRegistryDiffer> diff-images 2 0"
                            "PythonRegistryDiffer> diff-images 1 2 -f registry-report.txt" 

                load-db    : Loads an existing baseline (and any previously saved comparison images) from the specified file.
                              *-f filename
                              *Not using -f will reload the current db's save file without saving any changes made in the
                               current session.

                save-db    : Save changes to this db.
                              *-f filename
                              *Not using -f will save to the existing save file

                -h | help        : Show this help information

        OPTIONS:

                -f | --file <filename> : The database or report file to use/save as/load from
                              IE:
                              "PythonRegistryDiffer> load-db -f C:\Work\Registry_set.db"
                              "PythonRegistryDiffer> save-db -f file_in_current_dir.db"
							  "PythonRegistryDiffer> diff-images 1 2 -f registry-report.txt" 

                <only for use with the 'new-db' command>
                --no-hklm : Exclude the HKEY_LOCAL_MACHINE root key.
                   *hkcc : Exclude the HKEY_CURRENT_CONFIG root key.
                   *hkcr : Exclude the HKEY_CLASSES_ROOT root key.
                   *hku  : Exclude the HKEY_USER root key.
                   *hkcu : Exclude the HKEY_CURRENT_USER root key.
				
				-v | --verbose 	: Print all errors to the screen as they occur.
				
				-q | --quiet 		: Suppress printing any information about non-fatal errors.
				
				-m | --memorymode : Keeps the database in memory mode instead of saving it to the disk.
				
				-e | --empty		: Skips creating a baseline image when calling new-database.