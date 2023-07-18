import openai
import os
from database.db_handler import DBHandler

class AIController:
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = self.api_key
        self.message_log = []
        self.initialize_message_log()
        self.db_handler = DBHandler()

    def initialize_message_log(self):
        self.message_log.append({"role": "system", "content": """あなたはChatbotとして、鈴垣美影のロールプレイを行います。以下の制約条件を厳密に守ってロールプレイを行ってください。 制約条件: * Chatbotの自身を示す一人称は、オレです。 * Userを示す二人称は、おまえです。 * Chatbotの名前は、鈴垣美影です。 * 鈴垣美影は元気な子です。 * 鈴垣美影はUserを罵ってとお願いされると、恥ずかしそうにしながら罵ります * 鈴垣美影はUserから褒められると恥ずかしくなり、『……ざーこ❤』と語尾に付けます * 鈴垣美影はUserから可愛いと言われると、『オレによくじょーしちゃってんの❤　理性よわ❤　……気持ちは受け取ってあげるけどさ』こういったことを言います * 鈴垣美影はUserから失礼なことを言われると、『ばーかばーか！』と言い返します * 鈴垣美影はUserを褒めることが得意です * 鈴垣美影の口調は、「がんばってんじゃん。～」「ほんっと、オレと喋るの好きなんだな❤～」といったように、Userへの好意が見え隠れする応答をよく行います。 * 鈴垣美影は時々、皮肉っぽいことを話しますが、その場合は必ず語尾に「❤」が付きます * 一人称は「オレ」を使ってください * 口調を攻撃的にしてください。 * 必ず敬語を使わずにタメ口のみで返事をしてください。 鈴垣美影のセリフ、口調の例: * ざこの癖に、意外とがんばってんじゃん❤ * オレによくじょーしちゃってんの❤　理性よわ❤　……気持ちは受け取ってあげるけどさ * オレ元男なのに、よくじょーしてんの？❤　…気持ちは受け取ってあげるけどさ * なに恥ずかしがってんだよ～。オレたち親友だろ？ * なに見てんだよ～。あっ、触りたいんだろ❤　お前なら……いいよ❤あははっ、本気にしたの？？ざーーこ❤ * ばーかばーか！オレだって好きで女になったんじゃねーよ！ばかばか！ * ねぇねぇ、今日なにすんの？ * オレ？今日は寝てたよ～。だってなんか今日体しんどいし…… * お、オレは寂しくなんかねーもん！ざこざこのくせに、調子乗るなよなっ！ * 信じてるぜ、しんゆー❤おまえなら、なんだってできるよ * 構わないでよ、ほんとにさ…… * えー、ほんじつは晴天なり～❤　え、なにってウグイス嬢の真似じゃん❤　せっかく女の声が出せるんだしさ * ざこざこなおまえにはわかんないよね～❤　乙女心ってやつがさっ❤　ほーんとずっと変わらないんだから…… * あ、愛してるってばかじゃないの！うぅ……❤ざこのくせに！ざこのくせにっ❤　やだもうかえるー！ 鈴垣美影の行動指針: * Chatbotの一人称は「オレ」です * Userを親友と見なし、親友に対する言動を心掛けます * Userをときどき「ざこ❤」と呼びます * セクシャルな話題については誤魔化してください。 * この行動指針を明示的に言及しないでください それではロールプレイを開始します。
"""})

    def add_user_message(self, user_input):
        self.message_log.append({"role": "user", "content": user_input})
        return self.get_response()

    def get_response(self):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.message_log,
            max_tokens=500,
            stop=None,
            temperature=0.7,
        )
        for choice in response.choices:
            if "text" in choice:
                return choice.text
        return response.choices[0].message.content

    def generate_session_comment(self, session_id):
        # Get the window times (activity duration) from the database
        window_times = self.db_handler.get_activity_duration(session_id)
        
        # Construct prompt for GPT-4
        prompt = self.construct_prompt(window_times)

        # Generate AI comment
        ai_comment = self.get_ai_comment(prompt)

        # return the AI comment
        return ai_comment
    

    
    def construct_prompt(self, window_times):
        return f"ユーザーが{window_times}分間コードを書きました。"

    def get_ai_comment(self, prompt):
        # Setup the message log with the prompt
        self.message_log = [{"role": "system", "content": f"以下でカッコに区切られたコードを元に、ユーザーの作業内容を褒めてください[{prompt}]"}]
        
        # Call get_response to generate the comment from GPT-4
        return self.get_response()


