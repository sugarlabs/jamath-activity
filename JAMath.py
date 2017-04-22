from sugar.activity import activity

class JAMath(activity.Activity):
    def __init__(self,handle):
        activity.Activity.__init__(self,handle)
        from juego import main
	main.main()

