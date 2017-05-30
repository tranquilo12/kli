# Kaggle-CLI (kli)
An unoffical Kaggle CLI (with a config file, and some error checks) 

	Installation: pip install kli 
	
	kli supports making a config file with the command "kli make"
	The config file's location:  ~/.config/kli/kli.ini
	
	Set it up with your username and password with the command "kli setup"
		The password is hashed just to prevent over-the-shoulder attacks if/when you view your config file.
		(It is not a powerful hash so beware)
	
	Supports downloading any file in any competition with the command "kli dl --comp /c/comp_url" 
		Provided you have accepted the rules (which it checks for)
		You also have the power to select the files that you want to download
