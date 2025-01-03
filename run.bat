pipenv run dev
python scripts\process_m3u.py output\user_result.m3u output\user_cc_all.m3u
python scripts\filtermp2.py output\user_cc_all.m3u output\user_cc.m3u
git add output/user_cc.m3u output/user_result.m3u
git commit -m "update"
git push origin master