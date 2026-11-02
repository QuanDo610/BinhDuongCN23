# -*- coding: utf-8 -*-
"""
Script thu thập và tạo tệp 200 câu nói của các vĩ nhân trên thế giới
Xuất ra định dạng JSON chuẩn UTF-8 tại thư mục OUTPUT/cau_noi_vi_nhan.json
"""

import os
import json

QUOTES = [
    # =========================================================================
    # PHẦN 1: TRÍ TUỆ, HỌC HỎI & TRI THỨC (KNOWLEDGE & WISDOM) - 30 CÂU
    # =========================================================================
    {
        "id": 1,
        "author": "Albert Einstein",
        "author_en": "Albert Einstein",
        "author_title": "Nhà vật lý lý thuyết đoạt giải Nobel, cha đẻ thuyết tương đối",
        "era": "Thế kỷ 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Học từ ngày hôm qua, sống cho ngày hôm nay, hy vọng vào ngày mai. Điều quan trọng nhất là không bao giờ ngừng đặt câu hỏi.",
        "quote_en": "Learn from yesterday, live for today, hope for tomorrow. The important thing is not to stop questioning.",
        "source": "Tạp chí LIFE (1955)"
    },
    {
        "id": 2,
        "author": "Socrates",
        "author_en": "Socrates",
        "author_title": "Triết gia Hy Lạp cổ đại, người đặt nền móng triết học phương Tây",
        "era": "Thế kỷ thứ 5 TCN",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Tôi chỉ biết một điều duy nhất, đó là tôi không biết gì cả.",
        "quote_en": "I know that I am intelligent, because I know that I know nothing.",
        "source": "Biện hộ của Socrates (Plato)"
    },
    {
        "id": 3,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà tư tưởng, nhà giáo dục vĩ đại thời Xuân Thu, sáng lập Nho giáo",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Học mà không suy nghĩ thì mông lung, suy nghĩ mà không học thì hiểm nghèo.",
        "quote_en": "Learning without thought is labor lost; thought without learning is perilous.",
        "source": "Luận Ngữ (Vi Chính)"
    },
    {
        "id": 4,
        "author": "Leonardo da Vinci",
        "author_en": "Leonardo da Vinci",
        "author_title": "Thiên tài toàn năng thời Phục hưng (họa sĩ, nhà khoa học, nhà phát minh)",
        "era": "Thế kỷ 15 - 16",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Học hỏi là việc duy nhất mà tâm trí không bao giờ kiệt sức, không bao giờ sợ hãi và không bao giờ hối tiếc.",
        "quote_en": "Learning never exhausts the mind.",
        "source": "Sổ tay Leonardo da Vinci"
    },
    {
        "id": 5,
        "author": "Isaac Newton",
        "author_en": "Sir Isaac Newton",
        "author_title": "Nhà vật lý, toán học vĩ đại người Anh, người phát minh định luật vạn vật hấp dẫn",
        "era": "Thế kỷ 17 - 18",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Nếu tôi nhìn xa hơn những người khác, đó là vì tôi đã đứng trên vai của những người khổng lồ.",
        "quote_en": "If I have seen further it is by standing on the shoulders of Giants.",
        "source": "Thư gửi Robert Hooke (1675)"
    },
    {
        "id": 6,
        "author": "Aristotle",
        "author_en": "Aristotle",
        "author_title": "Triết gia Hy Lạp cổ đại, học trò của Plato, thầy của Alexander Đại đế",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Biết mình là khởi đầu của mọi sự khôn ngoan.",
        "quote_en": "Knowing yourself is the beginning of all wisdom.",
        "source": "Triết học Cổ điển Hy Lạp"
    },
    {
        "id": 7,
        "author": "Benjamin Franklin",
        "author_en": "Benjamin Franklin",
        "author_title": "Khai quốc công thần Hoa Kỳ, nhà khoa học, nhà ngoại giao xuất chúng",
        "era": "Thế kỷ 18",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Đầu tư vào tri thức luôn mang lại mức lãi suất cao nhất.",
        "quote_en": "An investment in knowledge pays the best interest.",
        "source": "Niên giám Poor Richard"
    },
    {
        "id": 8,
        "author": "Francis Bacon",
        "author_en": "Francis Bacon",
        "author_title": "Triết gia, chính khách người Anh, cha đẻ của phương pháp thực nghiệm",
        "era": "Thế kỷ 16 - 17",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Tri thức là sức mạnh.",
        "quote_en": "Knowledge is power.",
        "source": "Tác phẩm Meditationes Sacrae (1597)"
    },
    {
        "id": 9,
        "author": "Galileo Galilei",
        "author_en": "Galileo Galilei",
        "author_title": "Nhà thiên văn học, vật lý học người Ý, cha đẻ thiên văn quan sát hiện đại",
        "era": "Thế kỷ 16 - 17",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Bạn không thể dạy một người bất cứ điều gì; bạn chỉ có thể giúp người đó tìm thấy điều đó bên trong chính họ.",
        "quote_en": "You cannot teach a man anything; you can only help him find it within himself.",
        "source": "Đối thoại về hai hệ thống thế giới"
    },
    {
        "id": 10,
        "author": "Lão Tử",
        "author_en": "Laozi",
        "author_title": "Nhà triết học Trung Hoa cổ đại, người sáng lập Đạo giáo",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Kẻ biết người là người khôn ngoan; kẻ biết mình là người giác ngộ. Kẻ thắng người là có sức mạnh; kẻ thắng mình mới là người thực sự dũng cảm.",
        "quote_en": "Knowing others is intelligence; knowing yourself is true wisdom. Mastering others is strength; mastering yourself is true power.",
        "source": "Đạo Đức Kinh (Chương 33)"
    },
    {
        "id": 11,
        "author": "René Descartes",
        "author_en": "René Descartes",
        "author_title": "Nhà triết học, toán học người Pháp, cha đẻ triết học hiện đại",
        "era": "Thế kỷ 17",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Tôi tư duy, nên tôi tồn tại.",
        "quote_en": "I think, therefore I am. (Cogito, ergo sum)",
        "source": "Phương pháp luận (Discourse on the Method, 1637)"
    },
    {
        "id": 12,
        "author": "Marie Curie",
        "author_en": "Marie Curie",
        "author_title": "Nhà vật lý và hóa học, người đầu tiên giành 2 giải Nobel ở hai lĩnh vực khác nhau",
        "era": "Thế kỷ 19 - 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Trong cuộc sống không có gì đáng sợ, chỉ có những điều cần được thấu hiểu. Giờ là lúc hiểu nhiều hơn để bớt sợ hãi đi.",
        "quote_en": "Nothing in life is to be feared, it is only to be understood. Now is the time to understand more, so that we may fear less.",
        "source": "Hồi ký Marie Curie"
    },
    {
        "id": 13,
        "author": "Plato",
        "author_en": "Plato",
        "author_title": "Triết gia Hy Lạp cổ đại, sáng lập Viện Hàn lâm Athens",
        "era": "Thế kỷ thứ 5 - 4 TCN",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Người thông thái nói vì họ có điều gì đó để nói; kẻ ngốc nói chỉ vì họ phải nói điều gì đó.",
        "quote_en": "Wise men speak because they have something to say; fools because they have to say something.",
        "source": "Cộng hòa (The Republic)"
    },
    {
        "id": 14,
        "author": "Stephen Hawking",
        "author_en": "Stephen Hawking",
        "author_title": "Nhà vật lý lý thuyết, vũ trụ học xuất chúng người Anh",
        "era": "Thế kỷ 20 - 21",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Kẻ thù lớn nhất của tri thức không phải là sự dốt nát, mà chính là ảo tưởng về sự hiểu biết.",
        "quote_en": "The greatest enemy of knowledge is not ignorance, it is the illusion of knowledge.",
        "source": "Phát biểu báo chí (2001)"
    },
    {
        "id": 15,
        "author": "Albert Einstein",
        "author_en": "Albert Einstein",
        "author_title": "Nhà vật lý lý thuyết đoạt giải Nobel",
        "era": "Thế kỷ 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Trí tưởng tượng quan trọng hơn tri thức. Tri thức có giới hạn, còn trí tưởng tượng bao quát toàn thế giới.",
        "quote_en": "Imagination is more important than knowledge. For knowledge is limited, whereas imagination embraces the entire world.",
        "source": "Phỏng vấn trên The Saturday Evening Post (1929)"
    },
    {
        "id": 16,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà giáo dục vĩ đại thời Xuân Thu",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Ba người cùng đi, ắt có người là thầy của ta. Ta chọn lấy điều hay của họ mà theo, thấy điều dở của họ mà sửa mình.",
        "quote_en": "When I walk along with two others, they may serve me as my teachers. I will select their good qualities and follow them, their bad qualities and avoid them.",
        "source": "Luận Ngữ (Thuật Nhi)"
    },
    {
        "id": 17,
        "author": "Carl Sagan",
        "author_en": "Carl Sagan",
        "author_title": "Nhà thiên văn học, tác giả người Mỹ, người phổ biến khoa học vũ trụ",
        "era": "Thế kỷ 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Ở đâu đó ngoài kia, có một điều kỳ diệu lạ thường đang chờ được khám phá.",
        "quote_en": "Somewhere, something incredible is waiting to be known.",
        "source": "Cosmos (1980)"
    },
    {
        "id": 18,
        "author": "Blaise Pascal",
        "author_en": "Blaise Pascal",
        "author_title": "Nhà toán học, vật lý học, triết gia người Pháp",
        "era": "Thế kỷ 17",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Con người chỉ là một cây sậy, thứ yếu ớt nhất trong tự nhiên, nhưng là một cây sậy biết suy nghĩ.",
        "quote_en": "Man is but a reed, the most feeble thing in nature, but he is a thinking reed.",
        "source": "Tư tưởng (Pensées, 1670)"
    },
    {
        "id": 19,
        "author": "Richard Feynman",
        "author_en": "Richard Feynman",
        "author_title": "Nhà vật lý lý thuyết đoạt giải Nobel người Mỹ",
        "era": "Thế kỷ 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Nguyên tắc đầu tiên là bạn không được tự lừa dối chính mình, và bạn chính là người dễ bị bạn lừa dối nhất.",
        "quote_en": "The first principle is that you must not fool yourself and you are the easiest person to fool.",
        "source": "Bài giảng khai giảng Caltech (1974)"
    },
    {
        "id": 20,
        "author": "Tuân Tử",
        "author_en": "Xunzi",
        "author_title": "Nhà tư tưởng Nho gia kiệt xuất thời Chiến Quốc",
        "era": "Thế kỷ thứ 3 TCN",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Không nghe không bằng nghe, nghe không bằng thấy, thấy không bằng biết, biết không bằng thực hành. Học đến thực hành mới là tột bực.",
        "quote_en": "Tell me and I forget, teach me and I may remember, involve me and I learn.",
        "source": "Tuân Tử (Nho Hiệu)"
    },
    {
        "id": 21,
        "author": "Immanuel Kant",
        "author_en": "Immanuel Kant",
        "author_title": "Triết gia người Đức, đỉnh cao của thời kỳ Khai sáng",
        "era": "Thế kỷ 18",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Hãy dũng cảm dùng chính trí tuệ của bạn! Đó chính là phương châm của thời kỳ Khai sáng.",
        "quote_en": "Sapere aude! Have courage to use your own reason! That is the motto of enlightenment.",
        "source": "Trả lời câu hỏi: Khai sáng là gì? (1784)"
    },
    {
        "id": 22,
        "author": "Charles Darwin",
        "author_en": "Charles Darwin",
        "author_title": "Nhà tự nhiên học người Anh, cha đẻ thuyết tiến hóa",
        "era": "Thế kỷ 19",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Sự ngu dốt thường sinh ra sự tự tin nhiều hơn là tri thức: chính những người biết ít, chứ không phải người biết nhiều, mới quả quyết rằng vấn đề này hay vấn đề kia không bao giờ giải quyết được bằng khoa học.",
        "quote_en": "Ignorance more frequently begets confidence than does knowledge.",
        "source": "Nguồn gốc loài người (The Descent of Man, 1871)"
    },
    {
        "id": 23,
        "author": "Bertrand Russell",
        "author_en": "Bertrand Russell",
        "author_title": "Nhà triết học, toán học, nhà hoạt động hòa bình đoạt giải Nobel Văn học",
        "era": "Thế kỷ 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Vấn đề cốt lõi của thế giới là kẻ ngu xuẩn thì quá tự tin, còn người khôn ngoan lại đầy ắp những hoài nghi.",
        "quote_en": "The whole problem with the world is that fools and fanatics are always so certain of themselves, and wiser people so full of doubts.",
        "source": "Bài luận Triumph of Stupidity (1933)"
    },
    {
        "id": 24,
        "author": "Louis Pasteur",
        "author_en": "Louis Pasteur",
        "author_title": "Nhà vi sinh vật học, hóa học người Pháp, cha đẻ vắc-xin",
        "era": "Thế kỷ 19",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Trong lĩnh vực quan sát, cơ hội chỉ mỉm cười với những tâm trí đã có sự chuẩn bị kỹ càng.",
        "quote_en": "In the fields of observation chance favors only the prepared mind.",
        "source": "Bài phát biểu tại Đại học Lille (1854)"
    },
    {
        "id": 25,
        "author": "Thomas Aquinas",
        "author_en": "Thomas Aquinas",
        "author_title": "Nhà triết học, thần học thời Trung Cổ",
        "era": "Thế kỷ 13",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Hãy cẩn trọng trước người chỉ đọc duy nhất một cuốn sách.",
        "quote_en": "Beware of the person of one book.",
        "source": "Lời răn Thomas Aquinas"
    },
    {
        "id": 26,
        "author": "Mark Twain",
        "author_en": "Mark Twain",
        "author_title": "Đại văn hào, nhà hài hước người Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Điều khiến bạn gặp rắc rối không phải là những gì bạn không biết. Đó là những gì bạn biết chắc như đinh đóng cột, nhưng thực ra nó lại sai.",
        "quote_en": "It ain't what you don't know that gets you into trouble. It's what you know for sure that just ain't so.",
        "source": "Bút ký Mark Twain"
    },
    {
        "id": 27,
        "author": "Lý Bạch",
        "author_en": "Li Bai",
        "author_title": "Thi tiên vĩ đại thời Đường, Trung Quốc",
        "era": "Thế kỷ 8",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Thiên sinh ngã tài tất hữu dụng, thiên kim tán tận hoàn phục lai (Trời sinh ra tài của ta ắt có chỗ dùng, nghìn vàng tiêu hết rồi sẽ lại có).",
        "quote_en": "Heaven produced my talent, and it must have a purpose; a thousand pieces of gold scattered will return again.",
        "source": "Tương Tiến Tửu"
    },
    {
        "id": 28,
        "author": "Lê Quý Đôn",
        "author_en": "Le Quy Don",
        "author_title": "Nhà bác học lớn nhất thời phong kiến Việt Nam",
        "era": "Thế kỷ 18",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Dẫu có bạc vàng trăm vạn lượng, chẳng bằng kinh sử một vài pho.",
        "quote_en": "Even with millions in silver and gold, it is not worth a few classic books.",
        "source": "Vân Đài Loại Ngữ"
    },
    {
        "id": 29,
        "author": "Alan Turing",
        "author_en": "Alan Turing",
        "author_title": "Nhà toán học người Anh, cha đẻ ngành khoa học máy tính và trí tuệ nhân tạo",
        "era": "Thế kỷ 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Đôi khi chính những người mà không ai tưởng tượng nổi lại làm nên những điều không ai có thể tưởng tượng được.",
        "quote_en": "Sometimes it is the people no one can imagine anything of who do the things no one can imagine.",
        "source": "Tiểu sử Alan Turing"
    },
    {
        "id": 30,
        "author": "John Dewey",
        "author_en": "John Dewey",
        "author_title": "Nhà triết học, nhà cải cách giáo dục hàng đầu của Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Trí tuệ & Học hỏi",
        "quote_vi": "Giáo dục không phải là sự chuẩn bị cho cuộc sống; giáo dục chính là bản thân cuộc sống.",
        "quote_en": "Education is not preparation for life; education is life itself.",
        "source": "My Pedagogic Creed (1897)"
    },

    # =========================================================================
    # PHẦN 2: LÒNG KIÊN TRÌ, Ý CHÍ & NGHỊ LỰC (PERSEVERANCE & RESILIENCE) - 30 CÂU
    # =========================================================================
    {
        "id": 31,
        "author": "Thomas Edison",
        "author_en": "Thomas Edison",
        "author_title": "Nhà phát minh vĩ đại người Mỹ với hơn 1.093 bằng sáng chế",
        "era": "Thế kỷ 19 - 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Tôi không hề thất bại. Tôi chỉ vừa tìm ra 10.000 cách mà bóng đèn không hoạt động.",
        "quote_en": "I have not failed. I've just found 10,000 ways that won't work.",
        "source": "Phỏng vấn sáng chế bóng đèn sợi đốt"
    },
    {
        "id": 32,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Anh hùng giải phóng dân tộc, danh nhân văn hóa thế giới",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Không có việc gì khó, chỉ sợ lòng không bền. Đào núi và lấp biển, quyết chí ắt làm nên.",
        "quote_en": "Nothing is impossible with perseverance. Moving mountains and filling seas can be done with determination.",
        "source": "Thơ tặng Đội thanh niên xung phong (1951)"
    },
    {
        "id": 33,
        "author": "Winston Churchill",
        "author_en": "Winston Churchill",
        "author_title": "Thủ tướng Anh thời Thế chiến II, đoạt giải Nobel Văn học",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Thành công không phải là đích đến cuối cùng, thất bại cũng chẳng phải điều chí mạng: chính lòng can đảm để bước tiếp mới là điều đáng giá.",
        "quote_en": "Success is not final, failure is not fatal: it is the courage to continue that counts.",
        "source": "Diễn văn thời chiến"
    },
    {
        "id": 34,
        "author": "Nelson Mandela",
        "author_en": "Nelson Mandela",
        "author_title": "Tổng thống Nam Phi, lãnh tụ chống chủ nghĩa Apartheid, Nobel Hòa bình",
        "era": "Thế kỷ 20 - 21",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Mọi việc dường như luôn là bất khả thi cho đến khi nó được hoàn thành.",
        "quote_en": "It always seems impossible until it's done.",
        "source": "Tự truyện Long Walk to Freedom"
    },
    {
        "id": 35,
        "author": "Lão Tử",
        "author_en": "Laozi",
        "author_title": "Nhà tư tưởng Trung Hoa cổ đại",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Hành trình vạn dặm bắt đầu từ một bước chân.",
        "quote_en": "A journey of a thousand miles begins with a single step.",
        "source": "Đạo Đức Kinh (Chương 64)"
    },
    {
        "id": 36,
        "author": "Friedrich Nietzsche",
        "author_en": "Friedrich Nietzsche",
        "author_title": "Triết gia người Đức với tầm ảnh hưởng sâu rộng thế kỷ 19",
        "era": "Thế kỷ 19",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Điều gì không giết chết được tôi sẽ làm cho tôi mạnh mẽ hơn.",
        "quote_en": "What does not kill me makes me stronger.",
        "source": "Hoàng hôn của những thần tượng (Twilight of the Idols, 1889)"
    },
    {
        "id": 37,
        "author": "Helen Keller",
        "author_en": "Helen Keller",
        "author_title": "Nữ văn sĩ, nhà hoạt động xã hội khiếm thị và khiếm thính người Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Mặc dù thế giới đầy rẫy những đau khổ, nhưng nó cũng đầy ắp những cách vượt qua đau khổ đó.",
        "quote_en": "Although the world is full of suffering, it is also full of the overcoming of it.",
        "source": "Tác phẩm Optimism (1903)"
    },
    {
        "id": 38,
        "author": "Abraham Lincoln",
        "author_en": "Abraham Lincoln",
        "author_title": "Tổng thống thứ 16 của Hoa Kỳ, người giải phóng nô lệ",
        "era": "Thế kỷ 19",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Mối bận tâm lớn nhất của tôi không phải là bạn đã từng thất bại hay chưa, mà là bạn có hài lòng với sự thất bại đó hay không.",
        "quote_en": "My great concern is not whether you have failed, but whether you are content with your failure.",
        "source": "Thư tín tổng thống Lincoln"
    },
    {
        "id": 39,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà tư tưởng thời Xuân Thu",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Vinh quang lớn nhất trong cuộc đời không phải là không bao giờ vấp ngã, mà là biết đứng dậy sau mỗi lần ngã xuống.",
        "quote_en": "Our greatest glory is not in never falling, but in rising every time we fall.",
        "source": "Luận Ngữ"
    },
    {
        "id": 40,
        "author": "Thomas Edison",
        "author_en": "Thomas Edison",
        "author_title": "Nhà phát minh vĩ đại người Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Thiên tài chỉ có 1% là cảm hứng, còn 99% là mồ hôi nước mắt.",
        "quote_en": "Genius is one percent inspiration and ninety-nine percent perspiration.",
        "source": "Phỏng vấn trên Harper's Monthly (1932)"
    },
    {
        "id": 41,
        "author": "Winston Churchill",
        "author_en": "Winston Churchill",
        "author_title": "Thủ tướng Anh thời Thế chiến II",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Nếu bạn đang đi qua địa ngục, hãy tiếp tục bước đi.",
        "quote_en": "If you are going through hell, keep going.",
        "source": "Khẩu hiệu thời chiến"
    },
    {
        "id": 42,
        "author": "Walt Disney",
        "author_en": "Walt Disney",
        "author_title": "Nhà tiên phong ngành hoạt hình, người sáng lập đế chế The Walt Disney",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Tất cả ước mơ của chúng ta đều có thể trở thành hiện thực, nếu chúng ta có đủ lòng dũng cảm để theo đuổi chúng.",
        "quote_en": "All our dreams can come true, if we have the courage to pursue them.",
        "source": "Phát biểu kỷ niệm Disney"
    },
    {
        "id": 43,
        "author": "Seneca",
        "author_en": "Lucius Annaeus Seneca",
        "author_title": "Triết gia Khắc kỷ La Mã, chính khách và nhà viết kịch",
        "era": "Thế kỷ thứ 1",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Không phải vì mọi việc khó khăn mà chúng ta không dám; chính vì chúng ta không dám nên mọi việc mới trở nên khó khăn.",
        "quote_en": "It is not because things are difficult that we do not dare; it is because we do not dare that they are difficult.",
        "source": "Những bức thư đạo đức gửi Lucilius"
    },
    {
        "id": 44,
        "author": "Vincent van Gogh",
        "author_en": "Vincent van Gogh",
        "author_title": "Danh họa trường phái Hậu ấn tượng người Hà Lan",
        "era": "Thế kỷ 19",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Những điều vĩ đại không được tạo ra từ một xung động bộc phát, mà là tập hợp của nhiều điều nhỏ bé được gom góp lại cùng nhau.",
        "quote_en": "Great things are not done by impulse, but by a series of small things brought together.",
        "source": "Thư gửi em trai Theo van Gogh"
    },
    {
        "id": 45,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Anh hùng giải phóng dân tộc",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Gạo đem vào giã bao đau đớn, Gạo giã xong rồi trắng tựa bông. Sống ở trên đời người cũng vậy, Gian nan rèn luyện mới thành công.",
        "quote_en": "Pounding rice is full of agony, but once done, it is white like cotton. Such is life for humankind: through hardships and trials one achieves success.",
        "source": "Nhật ký trong tù (Bài 'Giã gạo')"
    },
    {
        "id": 46,
        "author": "Charles Darwin",
        "author_en": "Charles Darwin",
        "author_title": "Nhà tự nhiên học người Anh",
        "era": "Thế kỷ 19",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Không phải loài mạnh nhất hay thông minh nhất sẽ sống sót, mà là loài thích ứng tốt nhất với sự thay đổi.",
        "quote_en": "It is not the strongest of the species that survives, nor the most intelligent, but the one most responsive to change.",
        "source": "Nguồn gốc các loài (Paraphrase)"
    },
    {
        "id": 47,
        "author": "Babe Ruth",
        "author_en": "Babe Ruth",
        "author_title": "Huyền thoại bóng chày vĩ đại nhất lịch sử nước Mỹ",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Bạn không bao giờ có thể đánh bại một người không bao giờ chịu bỏ cuộc.",
        "quote_en": "It's hard to beat a person who never gives up.",
        "source": "Tự truyện Babe Ruth"
    },
    {
        "id": 48,
        "author": "Mạnh Tử",
        "author_en": "Mencius",
        "author_title": "Nhà triết học Nho gia vĩ đại thứ hai sau Khổng Tử (Á Thánh)",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Trời sắp giáng sứ mệnh lớn cho ai, trước hết phải làm khổ tâm chí, nhọc gân cốt, đói thể xác, hao tổn thân mình, làm rối loạn những việc người ấy làm, để rèn luyện tính tình, tăng thêm tài năng.",
        "quote_en": "When Heaven is about to confer a great responsibility on any man, it will exercise his mind with suffering, and his sinews and bones with toil.",
        "source": "Mạnh Tử (Cáo Tử hạ)"
    },
    {
        "id": 49,
        "author": "Marcus Aurelius",
        "author_en": "Marcus Aurelius",
        "author_title": "Hoàng đế La Mã, triết gia Khắc kỷ vĩ đại",
        "era": "Thế kỷ thứ 2",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Chướng ngại cản trở hành động sẽ thúc đẩy hành động. Điều đứng chắn trên đường sẽ trở thành con đường.",
        "quote_en": "The impediment to action advances action. What stands in the way becomes the way.",
        "source": "Suy tưởng (Meditations, Quyển 5)"
    },
    {
        "id": 50,
        "author": "Theodore Roosevelt",
        "author_en": "Theodore Roosevelt",
        "author_title": "Tổng thống thứ 26 của Hoa Kỳ, đoạt giải Nobel Hòa bình",
        "era": "Thế kỷ 19 - 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Hãy tin rằng bạn có thể làm được, và bạn đã đi được một nửa chặng đường rồi.",
        "quote_en": "Believe you can and you're halfway there.",
        "source": "Diễn văn của Theodore Roosevelt"
    },
    {
        "id": 51,
        "author": "Albert Einstein",
        "author_en": "Albert Einstein",
        "author_title": "Nhà vật lý lý thuyết đoạt giải Nobel",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Cuộc sống giống như đi xe đạp. Muốn giữ thăng bằng, bạn phải liên tục tiến về phía trước.",
        "quote_en": "Life is like riding a bicycle. To keep your balance, you must keep moving.",
        "source": "Thư gửi con trai Eduard (1930)"
    },
    {
        "id": 52,
        "author": "Victor Hugo",
        "author_en": "Victor Hugo",
        "author_title": "Đại văn hào người Pháp, tác giả 'Những người khốn khổ'",
        "era": "Thế kỷ 19",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Sự kiên trì chính là bí mật của mọi thắng lợi.",
        "quote_en": "Perseverance, secret of all triumphs.",
        "source": "Những người lao động biển (1866)"
    },
    {
        "id": 53,
        "author": "Trang Tử",
        "author_en": "Zhuangzi",
        "author_title": "Triết gia Đạo gia trứ danh thời Chiến Quốc",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Giếng cạn không thể nói chuyện biển cả với ếch; mùa hè ngắn ngủi không thể bàn về băng tuyết với côn trùng.",
        "quote_en": "You cannot talk about the ocean to a frog in a well; you cannot talk about ice to an insect of summer.",
        "source": "Trang Tử (Thu Thủy)"
    },
    {
        "id": 54,
        "author": "Napoleon Bonaparte",
        "author_en": "Napoleon Bonaparte",
        "author_title": "Hoàng đế Pháp, nhà quân sự kiệt xuất thế giới",
        "era": "Thế kỷ 18 - 19",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Từ 'bất khả thi' chỉ nằm trong từ điển của những kẻ ngốc nghếch.",
        "quote_en": "Impossible is a word to be found only in the dictionary of fools.",
        "source": "Phát ngôn quân sự Napoleon"
    },
    {
        "id": 55,
        "author": "Michael Jordan",
        "author_en": "Michael Jordan",
        "author_title": "Huyền thoại bóng rổ vĩ đại nhất mọi thời đại",
        "era": "Thế kỷ 20 - 21",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Tôi đã ném trượt hơn 9.000 cú ném trong sự nghiệp. Tôi đã thua gần 300 trận. 26 lần tôi được tin tưởng giao cú ném quyết định nhưng đã trượt. Tôi đã thất bại hết lần này đến lần khác. Và đó là lý do tôi thành công.",
        "quote_en": "I've failed over and over and over again in my life. And that is why I succeed.",
        "source": "Chiến dịch quảng cáo Nike (1997)"
    },
    {
        "id": 56,
        "author": "Viktor Frankl",
        "author_en": "Viktor E. Frankl",
        "author_title": "Bác sĩ tâm thần người Áo, tác giả sống sót qua trại tập trung Đức Quốc xã",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Người có một lý do để sống (chữ 'Tại sao') có thể chịu đựng được hầu như mọi hoàn cảnh (chữ 'Như thế nào').",
        "quote_en": "Those who have a 'why' to live, can bear with almost any 'how'.",
        "source": "Đi tìm lẽ sống (Man's Search for Meaning, 1946)"
    },
    {
        "id": 57,
        "author": "Haruki Murakami",
        "author_en": "Haruki Murakami",
        "author_title": "Tiểu thuyết gia đương đại nổi tiếng của Nhật Bản",
        "era": "Thế kỷ 20 - 21",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Nỗi đau là điều không thể tránh khỏi; nhưng chịu đựng đau khổ hay không là sự lựa chọn của bạn.",
        "quote_en": "Pain is inevitable. Suffering is optional.",
        "source": "Tôi nói gì khi nói về chạy bộ (2007)"
    },
    {
        "id": 58,
        "author": "Dale Carnegie",
        "author_en": "Dale Carnegie",
        "author_title": "Tác giả cuốn 'Đắc nhân tâm', bậc thầy nghệ thuật giao tiếp",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Hầu hết những điều quan trọng trên thế giới đều được hoàn thành bởi những người đã kiên trì cố gắng ngay cả khi dường như không còn chút hy vọng nào.",
        "quote_en": "Most of the important things in the world have been accomplished by people who have kept on trying when there seemed to be no hope at all.",
        "source": "Quẳng gánh lo đi và vui sống"
    },
    {
        "id": 59,
        "author": "Nguyễn Trãi",
        "author_en": "Nguyen Trai",
        "author_title": "Danh nhân văn hóa thế giới, anh hùng dân tộc, quân sư khởi nghĩa Lam Sơn",
        "era": "Thế kỷ 15",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Nếm mật nằm gai, há phải một hai sớm tối; Quên ăn vì giận, sách lược thao suy xét đã tinh.",
        "quote_en": "Tasting gall and sleeping on firewood, enduring year after year; forgetting food in anger, mastering every strategy of war.",
        "source": "Bình Ngô Đại Cáo (1428)"
    },
    {
        "id": 60,
        "author": "Robert Frost",
        "author_en": "Robert Frost",
        "author_title": "Nhà thơ người Mỹ 4 lần đoạt giải Pulitzer",
        "era": "Thế kỷ 20",
        "category": "Lòng kiên trì & Ý chí",
        "quote_vi": "Cách tốt nhất để đi qua nó là luôn luôn đi xuyên qua nó.",
        "quote_en": "The best way out is always through.",
        "source": "A Servant to Servants (1914)"
    },

    # =========================================================================
    # PHẦN 3: THÀNH CÔNG, SÁNG TẠO & KHÁT VỌNG (SUCCESS & INNOVATION) - 25 CÂU
    # =========================================================================
    {
        "id": 61,
        "author": "Steve Jobs",
        "author_en": "Steve Jobs",
        "author_title": "Nhà đồng sáng lập Apple, biểu tượng của sự đổi mới sáng tạo",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Hãy luôn khao khát, hãy cứ dại khờ.",
        "quote_en": "Stay hungry. Stay foolish.",
        "source": "Bài phát biểu tại Lễ tốt nghiệp ĐH Stanford (2005)"
    },
    {
        "id": 62,
        "author": "Bill Gates",
        "author_en": "Bill Gates",
        "author_title": "Nhà đồng sáng lập Microsoft, nhà từ thiện toàn cầu",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Nếu bạn sinh ra trong nghèo khó, đó không phải lỗi của bạn. Nhưng nếu bạn chết đi trong nghèo khó, đó hoàn toàn là lỗi của bạn.",
        "quote_en": "If you are born poor it's not your mistake, but if you die poor it's your mistake.",
        "source": "Phát biểu tại các diễn đàn khởi nghiệp"
    },
    {
        "id": 63,
        "author": "Warren Buffett",
        "author_en": "Warren Buffett",
        "author_title": "Nhà đầu tư huyền thoại, Chủ tịch Berkshire Hathaway",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Quy tắc số 1: Đừng bao giờ để mất tiền. Quy tắc số 2: Đừng bao giờ quên quy tắc số 1.",
        "quote_en": "Rule No. 1: Never lose money. Rule No. 2: Never forget rule No. 1.",
        "source": "Thư gửi cổ đông Berkshire Hathaway"
    },
    {
        "id": 64,
        "author": "Steve Jobs",
        "author_en": "Steve Jobs",
        "author_title": "Nhà đồng sáng lập Apple",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Cách duy nhất để làm nên sự nghiệp vĩ đại là yêu lấy việc bạn đang làm. Nếu bạn chưa tìm thấy nó, hãy tiếp tục tìm kiếm. Đừng dừng lại.",
        "quote_en": "The only way to do great work is to love what you do. If you haven't found it yet, keep looking. Don't settle.",
        "source": "Diễn văn Stanford (2005)"
    },
    {
        "id": 65,
        "author": "Henry Ford",
        "author_en": "Henry Ford",
        "author_title": "Nhà sáng lập Hãng xe Ford, người cách mạng hóa dây chuyền sản xuất",
        "era": "Thế kỷ 19 - 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Dù bạn nghĩ rằng bạn làm được hay không làm được, bạn đều đúng.",
        "quote_en": "Whether you think you can, or you think you can't – you're right.",
        "source": "Tạp chí The American Magazine (1947)"
    },
    {
        "id": 66,
        "author": "Walt Disney",
        "author_en": "Walt Disney",
        "author_title": "Nhà sáng lập Walt Disney",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Cách tốt nhất để bắt đầu là ngừng nói và bắt tay vào làm.",
        "quote_en": "The way to get started is to quit talking and begin doing.",
        "source": "Hồi ức Walt Disney"
    },
    {
        "id": 67,
        "author": "Albert Einstein",
        "author_en": "Albert Einstein",
        "author_title": "Nhà vật lý lý thuyết đoạt giải Nobel",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Đừng cố gắng trở thành một người thành công, mà hãy cố gắng trở thành một người có giá trị.",
        "quote_en": "Try not to become a man of success, but rather try to become a man of value.",
        "source": "Tạp chí LIFE (1955)"
    },
    {
        "id": 68,
        "author": "Jeff Bezos",
        "author_en": "Jeff Bezos",
        "author_title": "Nhà sáng lập tập đoàn thương mại điện tử Amazon",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Nếu bạn tăng số lượng thử nghiệm bạn thực hiện mỗi năm từ một trăm lên một nghìn, bạn sẽ nhân quy mô đổi mới của mình lên một cách ngoạn mục.",
        "quote_en": "If you double the number of experiments you do per year you're going to double your inventiveness.",
        "source": "Thư gửi cổ đông Amazon"
    },
    {
        "id": 69,
        "author": "Charlie Munger",
        "author_en": "Charlie Munger",
        "author_title": "Phó chủ tịch Berkshire Hathaway, nhà thông thái của giới tài chính",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Cách tốt nhất để có được thứ bạn muốn là hãy xứng đáng với thứ đó.",
        "quote_en": "The safest way to get what you want is to try and deserve what you want.",
        "source": "Poor Charlie's Almanack"
    },
    {
        "id": 70,
        "author": "Pablo Picasso",
        "author_en": "Pablo Picasso",
        "author_title": "Danh họa vĩ đại người Tây Ban Nha, đồng sáng lập trường phái Lập thể",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Hành động là chìa khóa nền tảng cho mọi thành công.",
        "quote_en": "Action is the foundational key to all success.",
        "source": "Ghi chép của Pablo Picasso"
    },
    {
        "id": 71,
        "author": "Peter Drucker",
        "author_en": "Peter Drucker",
        "author_title": "Cha đẻ của ngành quản trị kinh doanh hiện đại",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Cách tốt nhất để dự đoán tương lai là tự mình kiến tạo ra nó.",
        "quote_en": "The best way to predict the future is to create it.",
        "source": "Các tác phẩm về Quản trị học"
    },
    {
        "id": 72,
        "author": "Alexander Graham Bell",
        "author_en": "Alexander Graham Bell",
        "author_title": "Nhà phát minh người Scotland, sáng chế ra điện thoại",
        "era": "Thế kỷ 19 - 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Khi một cánh cửa đóng lại, một cánh cửa khác sẽ mở ra; nhưng chúng ta thường nhìn vào cánh cửa đã đóng quá lâu đến mức không thấy được cánh cửa đang mở ra cho mình.",
        "quote_en": "When one door closes, another opens; but we often look so long and so regretfully upon the closed door that we do not see the one which has opened for us.",
        "source": "Hồi ký Bell"
    },
    {
        "id": 73,
        "author": "Henry David Thoreau",
        "author_en": "Henry David Thoreau",
        "author_title": "Triết gia, nhà tự nhiên học người Mỹ, tác giả 'Walden'",
        "era": "Thế kỷ 19",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Thành công thường đến với những ai quá bận rộn để có thời gian tìm kiếm nó.",
        "quote_en": "Success usually comes to those who are too busy to be looking for it.",
        "source": "Nhật ký Walden"
    },
    {
        "id": 74,
        "author": "Sam Walton",
        "author_en": "Sam Walton",
        "author_title": "Nhà sáng lập chuỗi siêu thị Walmart",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Chỉ có duy nhất một ông chủ: đó là khách hàng. Ông ấy có thể sa thải tất cả mọi người trong công ty, từ chủ tịch cho tới nhân viên, chỉ bằng cách tiêu tiền ở nơi khác.",
        "quote_en": "There is only one boss. The customer. And he can fire everybody in the company from the chairman on down, simply by spending his money somewhere else.",
        "source": "Tự truyện Made in America"
    },
    {
        "id": 75,
        "author": "John D. Rockefeller",
        "author_en": "John D. Rockefeller",
        "author_title": "Ông trùm dầu mỏ người Mỹ, người giàu nhất lịch sử hiện đại",
        "era": "Thế kỷ 19 - 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Đừng ngại từ bỏ những điều tốt đẹp để vươn tới những điều vĩ đại.",
        "quote_en": "Don't be afraid to give up the good to go for the great.",
        "source": "Lời khuyên kinh doanh Rockefeller"
    },
    {
        "id": 76,
        "author": "Ray Kroc",
        "author_en": "Ray Kroc",
        "author_title": "Nhà sáng lập và phát triển đế chế McDonald's",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Không có gì trên thế giới có thể thay thế được lòng kiên trì. Tài năng không làm được. Thiên tài không làm được. Giáo dục cũng không. Chỉ lòng kiên trì và sự quyết tâm mới có sức mạnh vô song.",
        "quote_en": "Nothing in this world can take the place of persistence.",
        "source": "Grinding It Out (1977)"
    },
    {
        "id": 77,
        "author": "Steve Jobs",
        "author_en": "Steve Jobs",
        "author_title": "Nhà đồng sáng lập Apple",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Sự đổi mới là điều tạo ra sự khác biệt giữa người dẫn đầu và kẻ đi sau.",
        "quote_en": "Innovation distinguishes between a leader and a follower.",
        "source": "The Innovation Secrets of Steve Jobs"
    },
    {
        "id": 78,
        "author": "Oprah Winfrey",
        "author_en": "Oprah Winfrey",
        "author_title": "Nữ hoàng truyền thông, tỷ phú tự thân người Mỹ",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Bạn càng tôn vinh và ăn mừng cuộc sống của mình, cuộc sống càng cho bạn nhiều điều hơn để ăn mừng.",
        "quote_en": "The more you praise and celebrate your life, the more there is in life to celebrate.",
        "source": "Tạp chí O, The Oprah Magazine"
    },
    {
        "id": 79,
        "author": "Jack Ma",
        "author_en": "Jack Ma",
        "author_title": "Nhà sáng lập tập đoàn Alibaba",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Hôm nay đầy rẫy khó khăn, ngày mai còn tồi tệ hơn, nhưng ngày mốt sẽ là ánh mặt trời rực rỡ.",
        "quote_en": "Today is hard, tomorrow will be worse, but the day after tomorrow will be sunshine.",
        "source": "Diễn đàn Kinh tế Thế giới Davos"
    },
    {
        "id": 80,
        "author": "Nikola Tesla",
        "author_en": "Nikola Tesla",
        "author_title": "Nhà phát minh, kỹ sư điện thiên tài người Mỹ gốc Serbia",
        "era": "Thế kỷ 19 - 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Hiện tại là của họ; tương lai, nơi mà tôi thực sự cống hiến để tạo ra, là của tôi.",
        "quote_en": "The present is theirs; the future, for which I really worked, is mine.",
        "source": "Hồi ký Nikola Tesla"
    },
    {
        "id": 81,
        "author": "Warren Buffett",
        "author_en": "Warren Buffett",
        "author_title": "Nhà đầu tư huyền thoại",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Phải mất 20 năm để xây dựng danh tiếng và chỉ mất 5 phút để hủy hoại nó. Nếu bạn nghĩ về điều đó, bạn sẽ làm mọi việc khác đi.",
        "quote_en": "It takes 20 years to build a reputation and five minutes to ruin it. If you think about that, you'll do things differently.",
        "source": "Thư gửi cổ đông Berkshire Hathaway"
    },
    {
        "id": 82,
        "author": "Thomas J. Watson",
        "author_en": "Thomas J. Watson",
        "author_title": "Chủ tịch kiêm Tổng giám đốc huyền thoại của IBM",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Nếu bạn muốn tăng gấp đôi tỷ lệ thành công của mình, hãy tăng gấp đôi tỷ lệ thất bại.",
        "quote_en": "If you want to increase your success rate, double your failure rate.",
        "source": "Phương châm quản trị IBM"
    },
    {
        "id": 83,
        "author": "Richard Branson",
        "author_en": "Sir Richard Branson",
        "author_title": "Tỷ phú người Anh, nhà sáng lập Tập đoàn Virgin",
        "era": "Thế kỷ 20 - 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Cơ hội kinh doanh giống như những chuyến xe buýt, luôn luôn có một chuyến khác đang tới.",
        "quote_en": "Business opportunities are like buses, there's always another one coming.",
        "source": "Like a Virgin: Secrets They Won't Teach You at Business School"
    },
    {
        "id": 84,
        "author": "Vince Lombardi",
        "author_en": "Vince Lombardi",
        "author_title": "Huấn luyện viên bóng bầu dục huyền thoại người Mỹ",
        "era": "Thế kỷ 20",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Nơi duy nhất mà 'thành công' đứng trước 'lao động' là ở trong cuốn từ điển.",
        "quote_en": "The only place where success comes before work is in the dictionary.",
        "source": "Các bài diễn thuyết truyền cảm hứng của Lombardi"
    },
    {
        "id": 85,
        "author": "Simon Sinek",
        "author_en": "Simon Sinek",
        "author_title": "Tác giả, nhà tư vấn lãnh đạo người Mỹ gốc Anh",
        "era": "Thế kỷ 21",
        "category": "Thành công & Khát vọng",
        "quote_vi": "Mọi người không mua những gì bạn làm; họ mua lý do tại sao bạn làm điều đó.",
        "quote_en": "People don't buy what you do; they buy why you do it.",
        "source": "Bắt đầu với câu hỏi Tại sao (Start With Why, 2009)"
    },

    # =========================================================================
    # PHẦN 4: LÃNH ĐẠO, TRÁCH NHIỆM & TẦM NHÌN (LEADERSHIP & VISION) - 25 CÂU
    # =========================================================================
    {
        "id": 86,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Chủ tịch nước Việt Nam Dân chủ Cộng hòa",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Cán bộ là cái gốc của mọi công việc. Muôn việc thành công hoặc thất bại, đều do cán bộ tốt hoặc kém.",
        "quote_en": "Cadres are the root of all work. The success or failure of all endeavors depends on whether cadres are good or bad.",
        "source": "Sửa đổi lối làm việc (1947)"
    },
    {
        "id": 87,
        "author": "Tôn Tử",
        "author_en": "Sun Tzu",
        "author_title": "Danh tướng thời Xuân Thu, tác giả Binh pháp Tôn Tử",
        "era": "Thế kỷ thứ 5 TCN",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Biết người biết ta, trăm trận không nguy; không biết người mà biết ta, một thắng một bại; không biết người không biết ta, trận nào cũng bại.",
        "quote_en": "If you know the enemy and know yourself, you need not fear the result of a hundred battles.",
        "source": "Binh pháp Tôn Tử (Thiên Mưu Công)"
    },
    {
        "id": 88,
        "author": "Mahatma Gandhi",
        "author_en": "Mahatma Gandhi",
        "author_title": "Lãnh tụ phong trào giải phóng Ấn Độ bằng phương pháp bất bạo động",
        "era": "Thế kỷ 19 - 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Hãy trở thành sự thay đổi mà bạn muốn nhìn thấy trên thế giới này.",
        "quote_en": "Be the change that you wish to see in the world.",
        "source": "Các bài báo và bài phát biểu của Gandhi"
    },
    {
        "id": 89,
        "author": "Abraham Lincoln",
        "author_en": "Abraham Lincoln",
        "author_title": "Tổng thống thứ 16 của Hoa Kỳ",
        "era": "Thế kỷ 19",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Hầu hết mọi người đều có thể chịu đựng được nghịch cảnh, nhưng nếu bạn muốn thử thách tính cách của một con người, hãy trao cho người đó quyền lực.",
        "quote_en": "Nearly all men can stand adversity, but if you want to test a man's character, give him power.",
        "source": "Các câu nói nổi tiếng của Lincoln"
    },
    {
        "id": 90,
        "author": "John F. Kennedy",
        "author_en": "John F. Kennedy",
        "author_title": "Tổng thống thứ 35 của Hoa Kỳ",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Đừng hỏi tổ quốc có thể làm gì cho bạn; hãy tự hỏi bạn có thể làm gì cho tổ quốc của mình.",
        "quote_en": "Ask not what your country can do for you — ask what you can do for your country.",
        "source": "Diễn văn nhậm chức Tổng thống (1961)"
    },
    {
        "id": 91,
        "author": "Trần Hưng Đạo",
        "author_en": "Tran Hung Dao",
        "author_title": "Quốc công Tiết chế, đại danh tướng đánh tan 3 lần quân Nguyên Mông",
        "era": "Thế kỷ 13",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Khoan thư sức dân để làm kế sâu rễ bền gốc, đó là thượng sách giữ nước.",
        "quote_en": "Easing the people's burdens to build deep roots and a firm base is the supreme strategy to protect the nation.",
        "source": "Đại Việt Sử Ký Toàn Thư (Lời dặn vua Trần Anh Tông, 1300)"
    },
    {
        "id": 92,
        "author": "Martin Luther King Jr.",
        "author_en": "Martin Luther King Jr.",
        "author_title": "Nhà hoạt động nhân quyền vĩ đại người Mỹ, giải Nobel Hòa bình",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Thước đo tối hậu của một người không phải là vị trí anh ta đứng trong những khoảnh khắc thuận lợi và an nhàn, mà là vị trí anh ta đứng trong những thời khắc thử thách và tranh đấu.",
        "quote_en": "The ultimate measure of a man is not where he stands in moments of comfort and convenience, but where he stands at times of challenge and controversy.",
        "source": "Strength to Love (1963)"
    },
    {
        "id": 93,
        "author": "Lão Tử",
        "author_en": "Laozi",
        "author_title": "Nhà tư tưởng Trung Hoa cổ đại",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Người lãnh đạo giỏi nhất là khi việc đã thành công, thiên hạ đều nói: 'Chính chúng ta đã tự làm nên việc đó'.",
        "quote_en": "A leader is best when people barely know he exists... When his work is done, they will say: we did it ourselves.",
        "source": "Đạo Đức Kinh (Chương 17)"
    },
    {
        "id": 94,
        "author": "George Washington",
        "author_en": "George Washington",
        "author_title": "Tổng thống đầu tiên của Hợp chúng quốc Hoa Kỳ",
        "era": "Thế kỷ 18",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Hãy gắn bó với những người có phẩm chất tốt nếu bạn quý trọng danh dự của mình, bởi thà ở một mình còn hơn ở cùng một người xấu.",
        "quote_en": "Associate yourself with men of good quality if you esteem your own reputation; for 'tis better to be alone than in bad company.",
        "source": "Quy tắc ứng xử của George Washington"
    },
    {
        "id": 95,
        "author": "Dwight D. Eisenhower",
        "author_en": "Dwight D. Eisenhower",
        "author_title": "Thống tướng 5 sao, Tổng thống thứ 34 của Hoa Kỳ",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Lãnh đạo là nghệ thuật khiến người khác làm điều bạn muốn vì chính bản thân họ muốn làm điều đó.",
        "quote_en": "Leadership is the art of getting someone else to do something you want done because he wants to do it.",
        "source": "Phát biểu của Tổng thống Eisenhower"
    },
    {
        "id": 96,
        "author": "John C. Maxwell",
        "author_en": "John C. Maxwell",
        "author_title": "Chuyên gia hàng đầu thế giới về nghệ thuật lãnh đạo",
        "era": "Thế kỷ 20 - 21",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Một nhà lãnh đạo là người biết đường, đi trên con đường đó và chỉ đường cho người khác.",
        "quote_en": "A leader is one who knows the way, goes the way, and shows the way.",
        "source": "21 Nguyên Tắc Vàng Của Nghệ Thuật Lãnh Đạo"
    },
    {
        "id": 97,
        "author": "Nguyễn Trãi",
        "author_en": "Nguyen Trai",
        "author_title": "Danh nhân văn hóa thế giới",
        "era": "Thế kỷ 15",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Việc nhân nghĩa cốt ở yên dân, Quân điếu phạt trước lo trừ bạo.",
        "quote_en": "The foundation of benevolence and righteousness is to bring peace to the people; punitive military actions must first eliminate tyrannical oppression.",
        "source": "Bình Ngô Đại Cáo (1428)"
    },
    {
        "id": 98,
        "author": "Peter Drucker",
        "author_en": "Peter Drucker",
        "author_title": "Cha đẻ ngành quản trị kinh doanh",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Quản lý là làm đúng việc; lãnh đạo là làm việc đúng đắn.",
        "quote_en": "Management is doing things right; leadership is doing the right things.",
        "source": "The Effective Executive (1967)"
    },
    {
        "id": 99,
        "author": "Eleanor Roosevelt",
        "author_en": "Eleanor Roosevelt",
        "author_title": "Đệ nhất phu nhân Mỹ, nhà hoạt động ngoại giao và nhân quyền hàng đầu",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Tương lai thuộc về những ai tin tưởng vào vẻ đẹp trong ước mơ của mình.",
        "quote_en": "The future belongs to those who believe in the beauty of their dreams.",
        "source": "Các bài luận của Eleanor Roosevelt"
    },
    {
        "id": 100,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Chủ tịch nước Việt Nam Dân chủ Cộng hòa",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Dễ trăm lần không dân cũng chịu, Khó vạn lần dân liệu cũng xong.",
        "quote_en": "A hundred times easy, without the people it fails; ten thousand times hard, with the people it prevails.",
        "source": "Bài thơ dặn dò cán bộ"
    },
    {
        "id": 101,
        "author": "Tôn Tử",
        "author_en": "Sun Tzu",
        "author_title": "Tác giả Binh pháp Tôn Tử",
        "era": "Thế kỷ thứ 5 TCN",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Tướng giỏi là người thắng trận trước rồi mới giao chiến; tướng bại là người giao chiến trước rồi mới tìm cách cầu thắng.",
        "quote_en": "Victorious warriors win first and then go to war, while defeated warriors go to war first and then seek to win.",
        "source": "Binh pháp Tôn Tử (Thiên Quân Hình)"
    },
    {
        "id": 102,
        "author": "Colin Powell",
        "author_en": "Colin Powell",
        "author_title": "Đại tướng 4 sao, Ngoại trưởng Hoa Kỳ",
        "era": "Thế kỷ 20 - 21",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Không có bí quyết nào dẫn đến thành công. Nó là kết quả của sự chuẩn bị chu đáo, làm việc chăm chỉ và học hỏi từ những thất bại.",
        "quote_en": "There are no secrets to success. It is the result of preparation, hard work, and learning from failure.",
        "source": "Tự truyện My American Journey (1995)"
    },
    {
        "id": 103,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà tư tưởng thời Xuân Thu",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Kẻ thống trị mà dùng đức độ để trị dân thì như sao Bắc Đẩu, ở yên một chỗ mà muôn vì sao đều hướng về.",
        "quote_en": "He who exercises government by means of his virtue may be compared to the north polar star, which keeps its place and all the stars turn towards it.",
        "source": "Luận Ngữ (Vi Chính)"
    },
    {
        "id": 104,
        "author": "Theodore Roosevelt",
        "author_en": "Theodore Roosevelt",
        "author_title": "Tổng thống thứ 26 của Hoa Kỳ",
        "era": "Thế kỷ 19 - 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Người lãnh đạo giỏi nhất là người có đủ óc phán đoán để chọn người tài làm điều cần làm, và có đủ kiềm chế để không can thiệp vào khi họ đang làm.",
        "quote_en": "The best executive is the one who has sense enough to pick good men to do what he wants done, and self-restraint enough to keep from meddling with them while they do it.",
        "source": "Ghi chép của Theodore Roosevelt"
    },
    {
        "id": 105,
        "author": "Lý Thường Kiệt",
        "author_en": "Ly Thuong Kiet",
        "author_title": "Thái úy kiệt xuất thời Lý, người lãnh đạo kháng chiến chống Tống",
        "era": "Thế kỷ 11",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Nam quốc sơn hà Nam đế cư, Tiệt nhiên định phận tại thiên thư. Như hà nghịch lỗ lai xâm phạm, Nhữ đẳng hành khan thủ bại hư.",
        "quote_en": "The Southern mountains and rivers are ruled by the Southern Emperor; it is naturally settled in the Book of Heaven. If the reckless invaders dare to infringe, you shall witness your own complete defeat.",
        "source": "Bản tuyên ngôn độc lập đầu tiên (Sông Như Nguyệt, 1077)"
    },
    {
        "id": 106,
        "author": "Margaret Thatcher",
        "author_en": "Margaret Thatcher",
        "author_title": "Nữ Thủ tướng đầu tiên của Vương quốc Anh ('Bà đầm thép')",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Lãnh đạo cũng giống như một quý cô: nếu bạn phải nói với mọi người rằng mình là một quý cô, thì bạn không phải là một quý cô.",
        "quote_en": "Being powerful is like being a lady. If you have to tell people you are, you aren't.",
        "source": "Phỏng vấn truyền hình BBC"
    },
    {
        "id": 107,
        "author": "Alexander Đại Đế",
        "author_en": "Alexander the Great",
        "author_title": "Vua vĩ đại của vương quốc Macedonia cổ đại",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Tôi không sợ một đội quân sư tử được dẫn dắt bởi một con cừu; tôi chỉ sợ một đội quân cừu được dẫn dắt bởi một con sư tử.",
        "quote_en": "I am not afraid of an army of lions led by a sheep; I am afraid of an army of sheep led by a lion.",
        "source": "Biên niên sử Hy Lạp cổ đại"
    },
    {
        "id": 108,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Chủ tịch nước Việt Nam Dân chủ Cộng hòa",
        "era": "Thế kỷ 20",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Cần, Kiệm, Liêm, Chính, Chí công vô tư. Có tài mà không có đức là người vô dụng; có đức mà không có tài thì làm việc gì cũng khó.",
        "quote_en": "Diligence, Frugality, Integrity, and Righteousness, completely devoted to the public good. Talent without virtue makes a useless person; virtue without talent makes every endeavor difficult.",
        "source": "Nói chuyện với sinh viên, cán bộ (1955)"
    },
    {
        "id": 109,
        "author": "Simon Sinek",
        "author_en": "Simon Sinek",
        "author_title": "Nhà tư vấn lãnh đạo hàng đầu",
        "era": "Thế kỷ 21",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Lãnh đạo không phải là người đứng ở vị trí cao nhất. Lãnh đạo là người chịu trách nhiệm chăm lo cho những người đang được giao phó cho mình.",
        "quote_en": "Leadership is not about being in charge. It is about taking care of those in your charge.",
        "source": "Leaders Eat Last (2014)"
    },
    {
        "id": 110,
        "author": "Marcus Aurelius",
        "author_en": "Marcus Aurelius",
        "author_title": "Hoàng đế La Mã, triết gia Khắc kỷ",
        "era": "Thế kỷ thứ 2",
        "category": "Lãnh đạo & Trách nhiệm",
        "quote_vi": "Đừng lãng phí thêm thời gian tranh cãi về việc một người tốt nên như thế nào. Hãy là một người tốt.",
        "quote_en": "Waste no more time arguing about what a good man should be. Be one.",
        "source": "Suy tưởng (Meditations, Quyển 10)"
    },

    # =========================================================================
    # PHẦN 5: CUỘC SỐNG, Ý NGHĨA & HẠNH PHÚC (LIFE & HAPPINESS) - 25 CÂU
    # =========================================================================
    {
        "id": 111,
        "author": "Thích Nhất Hạnh",
        "author_en": "Thich Nhat Hanh",
        "author_title": "Thiền sư, nhà văn, nhà thơ, nhà hoạt động hòa bình quốc tế",
        "era": "Thế kỷ 20 - 21",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Hiện tại là giây phút duy nhất bạn thực sự có thể sống. Hãy mỉm cười, thở sâu và bước đi thật an lạc.",
        "quote_en": "The present moment is the only moment available to us, and it is the door to all moments.",
        "source": "Tác phẩm Phép lạ của sự tỉnh thức (1975)"
    },
    {
        "id": 112,
        "author": "Dalai Lama thứ 14",
        "author_en": "Dalai Lama XIV",
        "author_title": "Lãnh tụ tinh thần của Phật giáo Tây Tạng, giải Nobel Hòa bình",
        "era": "Thế kỷ 20 - 21",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Mục đích tối thượng của cuộc đời chúng ta là được hạnh phúc.",
        "quote_en": "The purpose of our lives is to be happy.",
        "source": "Nghệ thuật Hạnh phúc (The Art of Happiness, 1998)"
    },
    {
        "id": 113,
        "author": "Leo Tolstoy",
        "author_en": "Leo Tolstoy",
        "author_title": "Đại văn hào Nga, tác giả 'Chiến tranh và Hòa bình'",
        "era": "Thế kỷ 19 - 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Nếu bạn muốn được hạnh phúc, hãy là như vậy.",
        "quote_en": "If you want to be happy, be.",
        "source": "Nhật ký Leo Tolstoy"
    },
    {
        "id": 114,
        "author": "Aristotle",
        "author_en": "Aristotle",
        "author_title": "Triết gia Hy Lạp cổ đại",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Hạnh phúc là ý nghĩa và mục đích của cuộc sống, là toàn bộ mục tiêu và đích đến của sự tồn tại của con người.",
        "quote_en": "Happiness is the meaning and the purpose of life, the whole aim and end of human existence.",
        "source": "Đạo đức học Nicomachean"
    },
    {
        "id": 115,
        "author": "Marcus Aurelius",
        "author_en": "Marcus Aurelius",
        "author_title": "Hoàng đế La Mã, triết gia Khắc kỷ",
        "era": "Thế kỷ thứ 2",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Hạnh phúc của cuộc đời bạn phụ thuộc vào chất lượng những suy nghĩ của bạn.",
        "quote_en": "The happiness of your life depends upon the quality of your thoughts.",
        "source": "Suy tưởng (Meditations, Quyển 4)"
    },
    {
        "id": 116,
        "author": "Albert Schweitzer",
        "author_en": "Albert Schweitzer",
        "author_title": "Bác sĩ, triết gia, nhà thần học đoạt giải Nobel Hòa bình",
        "era": "Thế kỷ 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Thành công không phải là chìa khóa mở cánh cửa hạnh phúc. Hạnh phúc mới là chìa khóa dẫn tới thành công. Nếu bạn yêu điều bạn đang làm, bạn sẽ thành công.",
        "quote_en": "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful.",
        "source": "Triết học văn minh (1923)"
    },
    {
        "id": 117,
        "author": "Oscar Wilde",
        "author_en": "Oscar Wilde",
        "author_title": "Nhà văn, nhà soạn kịch kiệt xuất người Ireland",
        "era": "Thế kỷ 19",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Hãy là chính mình; những người khác đều đã có người làm rồi.",
        "quote_en": "Be yourself; everyone else is already taken.",
        "source": "Các tác phẩm kịch và châm ngôn của Oscar Wilde"
    },
    {
        "id": 118,
        "author": "Antoine de Saint-Exupéry",
        "author_en": "Antoine de Saint-Exupéry",
        "author_title": "Nhà văn, phi công người Pháp, tác giả 'Hoàng tử bé'",
        "era": "Thế kỷ 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Người ta chỉ nhìn thấy thật rõ ràng bằng trái tim. Những điều cốt yếu nhất thì mắt trần không thể thấy được.",
        "quote_en": "It is only with the heart that one can see rightly; what is essential is invisible to the eye.",
        "source": "Hoàng tử bé (The Little Prince, 1943)"
    },
    {
        "id": 119,
        "author": "Trang Tử",
        "author_en": "Zhuangzi",
        "author_title": "Triết gia Đạo gia thời Chiến Quốc",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Đời người sống giữa trời đất như con ngựa trắng chạy vụt qua khe cửa hẹp, thoắt một cái là qua.",
        "quote_en": "Human life between heaven and earth passes like a white colt leaping across a crevice, gone in an instant.",
        "source": "Trang Tử (Tri Bắc Du)"
    },
    {
        "id": 120,
        "author": "Fyodor Dostoevsky",
        "author_en": "Fyodor Dostoevsky",
        "author_title": "Đại văn hào Nga, tác giả 'Tội ác và Hình phạt'",
        "era": "Thế kỷ 19",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Bí mật của cuộc sống con người không phải chỉ là sống, mà là tìm thấy một lý do để sống.",
        "quote_en": "The mystery of human existence lies not in just staying alive, but in finding something to live for.",
        "source": "Anh em nhà Karamazov (1880)"
    },
    {
        "id": 121,
        "author": "Kahlil Gibran",
        "author_en": "Kahlil Gibran",
        "author_title": "Nhà thơ, triết gia người Liban, tác giả 'Ngôn sứ'",
        "era": "Thế kỷ 19 - 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Bạn càng để nỗi đau đào sâu vào tâm hồn mình, bạn càng có thể chứa đựng nhiều niềm vui hơn.",
        "quote_en": "The deeper that sorrow carves into your being, the more joy you can contain.",
        "source": "Ngôn sứ (The Prophet, 1923)"
    },
    {
        "id": 122,
        "author": "Victor Hugo",
        "author_en": "Victor Hugo",
        "author_title": "Đại văn hào người Pháp",
        "era": "Thế kỷ 19",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Hạnh phúc lớn nhất của cuộc đời là niềm tin chắc chắn rằng chúng ta được yêu thương — được yêu thương vì chính bản thân mình, hay nói đúng hơn, được yêu thương bất chấp bản thân mình.",
        "quote_en": "The greatest happiness of life is the conviction that we are loved; loved for ourselves, or rather, loved in spite of ourselves.",
        "source": "Những người khốn khổ (Les Misérables, 1862)"
    },
    {
        "id": 123,
        "author": "Ralph Waldo Emerson",
        "author_en": "Ralph Waldo Emerson",
        "author_title": "Nhà văn, triết gia người Mỹ, lãnh tụ phong trào Siêu việt luận",
        "era": "Thế kỷ 19",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Mục đích của cuộc sống không phải chỉ là để hạnh phúc. Nó là để trở nên hữu ích, để có danh dự, để có lòng trắc ẩn, và để cuộc đời bạn tạo ra được sự khác biệt.",
        "quote_en": "The purpose of life is not to be happy. It is to be useful, to be honorable, to be compassionate, to have it make some difference that you have lived and lived well.",
        "source": "Các bài luận của Emerson"
    },
    {
        "id": 124,
        "author": "Albert Camus",
        "author_en": "Albert Camus",
        "author_title": "Nhà văn, triết gia người Pháp đoạt giải Nobel Văn học",
        "era": "Thế kỷ 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Giữa mùa đông buốt giá tột cùng, cuối cùng tôi đã nhận ra bên trong mình có một mùa hè bất khả chiến bại.",
        "quote_en": "In the midst of winter, I found there was, within me, an invincible summer.",
        "source": "Mùa hè (L'Été, 1954)"
    },
    {
        "id": 125,
        "author": "William Shakespeare",
        "author_en": "William Shakespeare",
        "author_title": "Đại văn hào, nhà viết kịch vĩ đại nhất nước Anh",
        "era": "Thế kỷ 16 - 17",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Bản thân mọi thứ vốn không có gì tốt hay xấu, chỉ có suy nghĩ của chúng ta làm cho nó trở nên như vậy mà thôi.",
        "quote_en": "There is nothing either good or bad, but thinking makes it so.",
        "source": "Hamlet (Hồi 2, Cảnh 2)"
    },
    {
        "id": 126,
        "author": "George Bernard Shaw",
        "author_en": "George Bernard Shaw",
        "author_title": "Nhà viết kịch người Ireland đoạt giải Nobel Văn học và giải Oscar",
        "era": "Thế kỷ 19 - 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Cuộc sống không phải là đi tìm chính mình. Cuộc sống là đi tạo ra chính mình.",
        "quote_en": "Life isn't about finding yourself. Life is about creating yourself.",
        "source": "Châm ngôn George Bernard Shaw"
    },
    {
        "id": 127,
        "author": "Helen Keller",
        "author_en": "Helen Keller",
        "author_title": "Nữ văn sĩ, nhà hoạt động xã hội người Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Cuộc sống là một chuyến phiêu lưu táo bạo, hoặc nó chẳng là gì cả.",
        "quote_en": "Life is either a daring adventure or nothing at all.",
        "source": "The Open Door (1957)"
    },
    {
        "id": 128,
        "author": "Mẹ Teresa",
        "author_en": "Mother Teresa",
        "author_title": "Nữ tu Công giáo người Albania, giải Nobel Hòa bình, thánh tử vì đạo bác ái",
        "era": "Thế kỷ 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Không phải tất cả chúng ta đều có thể làm những điều vĩ đại. Nhưng chúng ta có thể làm những điều nhỏ bé với một tình yêu vĩ đại.",
        "quote_en": "Not all of us can do great things. But we can do small things with great love.",
        "source": "Lời răn của Mẹ Teresa"
    },
    {
        "id": 129,
        "author": "Lão Tử",
        "author_en": "Laozi",
        "author_title": "Nhà tư tưởng Trung Hoa cổ đại",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Biết đủ là người giàu có nhất. Người biết đủ thì thường an vui.",
        "quote_en": "He who is contented is rich.",
        "source": "Đạo Đức Kinh (Chương 33)"
    },
    {
        "id": 130,
        "author": "John Lennon",
        "author_en": "John Lennon",
        "author_title": "Huyền thoại âm nhạc ban nhạc The Beatles, nhà hoạt động hòa bình",
        "era": "Thế kỷ 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Khi tôi lên 5 tuổi, mẹ tôi luôn bảo tôi rằng hạnh phúc là chìa khóa của cuộc sống. Khi tôi đến trường, họ hỏi tôi muốn làm gì khi lớn lên. Tôi viết: 'Hạnh phúc'. Họ bảo tôi không hiểu đề bài, tôi nói họ không hiểu cuộc sống.",
        "quote_en": "When I was 5 years old, my mother always told me that happiness was the key to life. When I went to school, they asked me what I wanted to be when I grew up. I wrote down 'happy'. They told me I didn't understand the assignment, and I told them they didn't understand life.",
        "source": "Hồi ức John Lennon"
    },
    {
        "id": 131,
        "author": "Epictetus",
        "author_en": "Epictetus",
        "author_title": "Triết gia Khắc kỷ Hy Lạp cổ đại",
        "era": "Thế kỷ thứ 1 - 2",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Chúng ta không thể lựa chọn những hoàn cảnh bên ngoài xảy đến với mình, nhưng chúng ta luôn có thể lựa chọn cách mà mình phản ứng lại với chúng.",
        "quote_en": "Men are disturbed not by things, but by the view which they take of them.",
        "source": "Enchiridion (Sách hướng dẫn Khắc kỷ)"
    },
    {
        "id": 132,
        "author": "Abraham Lincoln",
        "author_en": "Abraham Lincoln",
        "author_title": "Tổng thống thứ 16 của Hoa Kỳ",
        "era": "Thế kỷ 19",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Đa số mọi người đều cảm thấy hạnh phúc đúng bằng mức độ mà họ quyết định trong tâm trí của họ.",
        "quote_en": "Most folks are about as happy as they make up their minds to be.",
        "source": "Ghi chép của Lincoln"
    },
    {
        "id": 133,
        "author": "Thích Nhất Hạnh",
        "author_en": "Thich Nhat Hanh",
        "author_title": "Thiền sư Việt Nam",
        "era": "Thế kỷ 20 - 21",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Không có con đường nào đi đến hạnh phúc: hạnh phúc chính là con đường.",
        "quote_en": "There is no way to peace, peace is the way. There is no way to happiness, happiness is the way.",
        "source": "Tác phẩm Peace Is Every Step"
    },
    {
        "id": 134,
        "author": "C.S. Lewis",
        "author_en": "C.S. Lewis",
        "author_title": "Nhà văn, học giả người Anh, tác giả 'Biên niên sử Narnia'",
        "era": "Thế kỷ 20",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Bạn không bao giờ quá già để đặt ra một mục tiêu mới hay mơ một giấc mơ mới.",
        "quote_en": "You are never too old to set another goal or to dream a new dream.",
        "source": "Thư tín C.S. Lewis"
    },
    {
        "id": 135,
        "author": "Baruch Spinoza",
        "author_en": "Baruch Spinoza",
        "author_title": "Triết gia người Hà Lan gốc Do Thái, người mở đầu triết học Khai sáng",
        "era": "Thế kỷ 17",
        "category": "Cuộc sống & Hạnh phúc",
        "quote_vi": "Hòa bình không phải là sự vắng bóng của chiến tranh, mà là một đức tính xuất phát từ sức mạnh của tâm hồn.",
        "quote_en": "Peace is not an absence of war, it is a virtue, a state of mind, a disposition for benevolence, confidence, justice.",
        "source": "Tractatus Politicus (1677)"
    },

    # =========================================================================
    # PHẦN 6: KỶ LUẬT, THỜI GIAN & HÀNH ĐỘNG (DISCIPLINE, TIME & ACTION) - 25 CÂU
    # =========================================================================
    {
        "id": 136,
        "author": "Benjamin Franklin",
        "author_en": "Benjamin Franklin",
        "author_title": "Khai quốc công thần Hoa Kỳ",
        "era": "Thế kỷ 18",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Bạn có yêu cuộc sống không? Vậy thì đừng lãng phí thời gian, vì đó là chất liệu làm nên cuộc sống.",
        "quote_en": "Dost thou love life? Then do not squander time, for that is the stuff life is made of.",
        "source": "Niên giám Poor Richard (1746)"
    },
    {
        "id": 137,
        "author": "Seneca",
        "author_en": "Lucius Annaeus Seneca",
        "author_title": "Triết gia Khắc kỷ La Mã",
        "era": "Thế kỷ thứ 1",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Không phải chúng ta có ít thời gian để sống, mà là do chúng ta đã lãng phí quá nhiều thời gian.",
        "quote_en": "It is not that we have a short time to live, but that we waste a lot of it.",
        "source": "Về sự ngắn ngủi của đời người (De Brevitate Vitae)"
    },
    {
        "id": 138,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà tư tưởng thời Xuân Thu",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Người không lo xa, ắt có buồn gần.",
        "quote_en": "If a man takes no thought about what is distant, he will find sorrow near at hand.",
        "source": "Luận Ngữ (Vệ Linh Công)"
    },
    {
        "id": 139,
        "author": "Bruce Lee",
        "author_en": "Bruce Lee (Lý Tiểu Long)",
        "author_title": "Huyền thoại võ thuật thế giới, người sáng lập Triệt Quyền Đạo",
        "era": "Thế kỷ 20",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Biết thôi chưa đủ, phải áp dụng. Muốn thôi chưa đủ, phải hành động.",
        "quote_en": "Knowing is not enough, we must apply. Willing is not enough, we must do.",
        "source": "Ghi chép võ thuật Lý Tiểu Long"
    },
    {
        "id": 140,
        "author": "Abraham Lincoln",
        "author_en": "Abraham Lincoln",
        "author_title": "Tổng thống thứ 16 của Hoa Kỳ",
        "era": "Thế kỷ 19",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Hãy cho tôi sáu giờ để đốn ngã một cái cây, và tôi sẽ dành bốn giờ đầu tiên để mài chiếc rìu thật sắc.",
        "quote_en": "Give me six hours to chop down a tree and I will spend the first four sharpening the axe.",
        "source": "Châm ngôn quản lý thời gian của Lincoln"
    },
    {
        "id": 141,
        "author": "Johann Wolfgang von Goethe",
        "author_en": "Johann Wolfgang von Goethe",
        "author_title": "Đại thi hào người Đức, tác giả kiệt tác 'Faust'",
        "era": "Thế kỷ 18 - 19",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Bất cứ điều gì bạn có thể làm, hay mơ ước mình có thể làm, hãy bắt đầu ngay đi. Sự táo bạo luôn mang trong mình thiên tài, sức mạnh và phép màu.",
        "quote_en": "Whatever you can do, or dream you can, begin it. Boldness has genius, power, and magic in it.",
        "source": "Tác phẩm Faust"
    },
    {
        "id": 142,
        "author": "Benjamin Franklin",
        "author_en": "Benjamin Franklin",
        "author_title": "Khai quốc công thần Hoa Kỳ",
        "era": "Thế kỷ 18",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Đừng bao giờ để đến ngày mai những việc bạn có thể làm trong ngày hôm nay.",
        "quote_en": "Never leave that till tomorrow which you can do today.",
        "source": "Niên giám Poor Richard"
    },
    {
        "id": 143,
        "author": "Jim Rohn",
        "author_en": "Jim Rohn",
        "author_title": "Diễn giả truyền cảm hứng, tác giả kinh điển về phát triển cá nhân",
        "era": "Thế kỷ 20 - 21",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Kỷ luật là chiếc cầu nối giữa mục tiêu và thành quả.",
        "quote_en": "Discipline is the bridge between goals and accomplishment.",
        "source": "7 Chiến lược cho Sự thịnh vượng và Hạnh phúc"
    },
    {
        "id": 144,
        "author": "Stephen Covey",
        "author_en": "Stephen R. Covey",
        "author_title": "Tác giả cuốn sách kinh điển '7 Thói quen của người thành đạt'",
        "era": "Thế kỷ 20 - 21",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Chìa khóa không phải là ưu tiên những gì nằm trên lịch làm việc của bạn, mà là lên lịch cho những điều ưu tiên nhất của bạn.",
        "quote_en": "The key is not to prioritize what's on your schedule, but to schedule your priorities.",
        "source": "The 7 Habits of Highly Effective People (1989)"
    },
    {
        "id": 145,
        "author": "Leonardo da Vinci",
        "author_en": "Leonardo da Vinci",
        "author_title": "Thiên tài toàn năng thời Phục hưng",
        "era": "Thế kỷ 15 - 16",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Tôi luôn bị ấn tượng bởi sự cấp bách của hành động. Biết thôi là chưa đủ; ta phải áp dụng. Sẵn sàng thôi là chưa đủ; ta phải làm.",
        "quote_en": "I have been impressed with the urgency of doing. Knowing is not enough; we must apply. Being willing is not enough; we must do.",
        "source": "Sổ tay Leonardo da Vinci"
    },
    {
        "id": 146,
        "author": "Marcus Aurelius",
        "author_en": "Marcus Aurelius",
        "author_title": "Hoàng đế La Mã, triết gia Khắc kỷ",
        "era": "Thế kỷ thứ 2",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Hãy làm mỗi hành động trong cuộc đời bạn như thể đó là hành động cuối cùng của bạn.",
        "quote_en": "Do every act of your life as though it were the very last act of your life.",
        "source": "Suy tưởng (Meditations, Quyển 2)"
    },
    {
        "id": 147,
        "author": "William Shakespeare",
        "author_en": "William Shakespeare",
        "author_title": "Đại văn hào người Anh",
        "era": "Thế kỷ 16 - 17",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Tôi đã lãng phí thời gian, và giờ đây thời gian đang làm hao mòn chính tôi.",
        "quote_en": "I wasted time, and now doth time waste me.",
        "source": "Richard II (Hồi 5, Cảnh 5)"
    },
    {
        "id": 148,
        "author": "Lão Tử",
        "author_en": "Laozi",
        "author_title": "Nhà tư tưởng Trung Hoa cổ đại",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Tự nhiên không bao giờ vội vã, thế mà vạn vật đều được hoàn thành một cách hoàn mỹ.",
        "quote_en": "Nature does not hurry, yet everything is accomplished.",
        "source": "Đạo Đức Kinh"
    },
    {
        "id": 149,
        "author": "Napoleon Hill",
        "author_en": "Napoleon Hill",
        "author_title": "Tác giả kinh điển cuốn sách 'Nghĩ giàu và Làm giàu' (Think and Grow Rich)",
        "era": "Thế kỷ 20",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Đừng chờ đợi. Thời điểm sẽ không bao giờ là 'vừa đúng' cả. Hãy bắt đầu ngay tại vị trí bạn đang đứng, với bất kỳ công cụ nào bạn có.",
        "quote_en": "Do not wait. The time will never be 'just right.' Start where you stand, and work with whatever tools you may have at your command.",
        "source": "Think and Grow Rich (1937)"
    },
    {
        "id": 150,
        "author": "Aristotle",
        "author_en": "Aristotle",
        "author_title": "Triết gia Hy Lạp cổ đại",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Chúng ta chính là những gì chúng ta lặp đi lặp lại hàng ngày. Do đó, sự xuất sắc không phải là một hành động đơn lẻ, mà là một thói quen.",
        "quote_en": "We are what we repeatedly do. Excellence, then, is not an act, but a habit.",
        "source": "Đạo đức học Nicomachean (Ý niệm qua Will Durant)"
    },
    {
        "id": 151,
        "author": "J.K. Rowling",
        "author_en": "J.K. Rowling",
        "author_title": "Nữ nhà văn người Anh, tác giả bộ truyện Harry Potter",
        "era": "Thế kỷ 20 - 21",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Chính những lựa chọn của chúng ta, chứ không phải năng lực, mới thể hiện con người thực sự của chúng ta.",
        "quote_en": "It is our choices that show what we truly are, far more than our abilities.",
        "source": "Harry Potter và Phòng chứa bí mật"
    },
    {
        "id": 152,
        "author": "Bruce Lee",
        "author_en": "Bruce Lee",
        "author_title": "Huyền thoại võ thuật thế giới",
        "era": "Thế kỷ 20",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Tôi không sợ người luyện 10.000 cú đá khác nhau một lần. Tôi chỉ sợ người luyện duy nhất một cú đá 10.000 lần.",
        "quote_en": "I fear not the man who has practiced 10,000 kicks once, but I fear the man who has practiced one kick 10,000 times.",
        "source": "Triết lý Triệt Quyền Đạo"
    },
    {
        "id": 153,
        "author": "Seneca",
        "author_en": "Lucius Annaeus Seneca",
        "author_title": "Triết gia Khắc kỷ La Mã",
        "era": "Thế kỷ thứ 1",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Trong khi chúng ta đang trì hoãn, cuộc sống vẫn cứ lặng lẽ trôi qua.",
        "quote_en": "While we are postponing, life speeds by.",
        "source": "Những bức thư đạo đức gửi Lucilius (Bức thư 1)"
    },
    {
        "id": 154,
        "author": "Henry Ford",
        "author_en": "Henry Ford",
        "author_title": "Nhà sáng lập Hãng xe Ford",
        "era": "Thế kỷ 19 - 20",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Bạn không thể xây dựng danh tiếng dựa trên những gì bạn dự định sẽ làm.",
        "quote_en": "You can't build a reputation on what you are going to do.",
        "source": "Châm ngôn kinh doanh của Henry Ford"
    },
    {
        "id": 155,
        "author": "Victor Hugo",
        "author_en": "Victor Hugo",
        "author_title": "Đại văn hào người Pháp",
        "era": "Thế kỷ 19",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Không có đội quân nào có thể ngăn cản một ý tưởng đã đến thời điểm của nó.",
        "quote_en": "Nothing is more powerful than an idea whose time has come.",
        "source": "Lịch sử của một tội ác (1877)"
    },
    {
        "id": 156,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Chủ tịch nước Việt Nam Dân chủ Cộng hòa",
        "era": "Thế kỷ 20",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Thực hành tiết kiệm thời giờ là một điều cực kỳ quan trọng. Ai lãng phí thời giờ là lãng phí tài sản của nhân dân.",
        "quote_en": "Practicing the economy of time is extremely important. Wasting time is squandering the wealth of the people.",
        "source": "Bài viết về Cần Kiệm Liêm Chính (1949)"
    },
    {
        "id": 157,
        "author": "Mark Twain",
        "author_en": "Mark Twain",
        "author_title": "Đại văn hào người Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Bí quyết để tiến về phía trước là bắt đầu. Bí quyết để bắt đầu là chia nhỏ công việc phức tạp thành các việc nhỏ dễ xử lý, rồi bắt tay vào làm việc đầu tiên.",
        "quote_en": "The secret of getting ahead is getting started. The secret of getting started is breaking your complex overwhelming tasks into small manageable tasks, and starting on the first one.",
        "source": "Ghi chép của Mark Twain"
    },
    {
        "id": 158,
        "author": "Tô Đông Pha",
        "author_en": "Su Shi (Su Dongpo)",
        "author_title": "Đại văn hào, nhà thơ kiệt xuất thời Bắc Tống, Trung Quốc",
        "era": "Thế kỷ 11",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Cổ chi lập đại sự giả, bất duy hữu siêu thế chi tài, diệc tất hữu kiên nhẫn bất bạt chi chí (Người làm nên việc lớn thời xưa, không chỉ có tài năng xuất chúng, mà ắt phải có ý chí kiên định không gì lay chuyển nổi).",
        "quote_en": "Those who accomplished great things in ancient times not only possessed exceptional talent, but inevitably possessed unyielding perseverance.",
        "source": "Triệu Thố Luận"
    },
    {
        "id": 159,
        "author": "Pablo Picasso",
        "author_en": "Pablo Picasso",
        "author_title": "Danh họa vĩ đại người Tây Ban Nha",
        "era": "Thế kỷ 20",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Cảm hứng có tồn tại, nhưng nó phải tìm thấy bạn khi bạn đang làm việc.",
        "quote_en": "Inspiration exists, but it has to find you working.",
        "source": "Phỏng vấn nghệ thuật Picasso"
    },
    {
        "id": 160,
        "author": "H. Jackson Brown Jr.",
        "author_en": "H. Jackson Brown Jr.",
        "author_title": "Tác giả cuốn cẩm nang cuộc sống bán chạy nhất thế giới",
        "era": "Thế kỷ 20 - 21",
        "category": "Kỷ luật & Thời gian",
        "quote_vi": "Đừng nói rằng bạn không có đủ thời gian. Bạn có chính xác cùng số giờ mỗi ngày như Helen Keller, Pasteur, Michelangelo, Mẹ Teresa, Leonardo da Vinci, Thomas Jefferson và Albert Einstein.",
        "quote_en": "Don't say you don't have enough time. You have exactly the same number of hours per day that were given to Helen Keller, Pasteur, Michelangelo, Mother Teresa, Leonardo da Vinci, Thomas Jefferson, and Albert Einstein.",
        "source": "Life's Little Instruction Book"
    },

    # =========================================================================
    # PHẦN 7: ĐẠO ĐỨC, NHÂN ÁI & NHÂN CÁCH (VIRTUE, KINDNESS & HUMANITY) - 25 CÂU
    # =========================================================================
    {
        "id": 161,
        "author": "Mahatma Gandhi",
        "author_en": "Mahatma Gandhi",
        "author_title": "Lãnh tụ vĩ đại người Ấn Độ",
        "era": "Thế kỷ 19 - 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Mắt đền mắt chỉ khiến cho cả thế giới này trở nên mù lòa.",
        "quote_en": "An eye for an eye will only make the whole world blind.",
        "source": "Triết lý bất bạo động (Ahimsa)"
    },
    {
        "id": 162,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà tư tưởng thời Xuân Thu",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Kỷ sở bất dục, vật thi ư nhân (Điều gì mình không muốn, đừng làm cho người khác).",
        "quote_en": "What you do not want done to yourself, do not do to others.",
        "source": "Luận Ngữ (Vệ Linh Công)"
    },
    {
        "id": 163,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Chủ tịch nước Việt Nam Dân chủ Cộng hòa",
        "era": "Thế kỷ 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Đạo đức cách mạng không phải trên trời sa xuống. Nó do đấu tranh, rèn luyện bền bỉ hàng ngày mà phát triển và củng cố. Cũng như ngọc càng mài càng sáng, vàng càng luyện càng trong.",
        "quote_en": "Revolutionary morality does not fall from the sky. It develops and consolidates through persistent daily struggle and training. Just as jade becomes brighter the more it is polished, gold becomes purer the more it is refined.",
        "source": "Bài viết Đạo đức cách mạng (1958)"
    },
    {
        "id": 164,
        "author": "Mẹ Teresa",
        "author_en": "Mother Teresa",
        "author_title": "Vị thánh của người nghèo, giải Nobel Hòa bình",
        "era": "Thế kỷ 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Nếu bạn phán xét người khác, bạn sẽ không còn thời gian để yêu thương họ nữa.",
        "quote_en": "If you judge people, you have no time to love them.",
        "source": "Các bài phát biểu của Mẹ Teresa"
    },
    {
        "id": 165,
        "author": "Martin Luther King Jr.",
        "author_en": "Martin Luther King Jr.",
        "author_title": "Nhà hoạt động nhân quyền người Mỹ",
        "era": "Thế kỷ 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Bóng tối không thể xua tan bóng tối; chỉ có ánh sáng mới làm được điều đó. Hận thù không thể xua tan hận thù; chỉ có tình yêu thương mới làm được điều đó.",
        "quote_en": "Darkness cannot drive out darkness; only light can do that. Hate cannot drive out hate; only love can do that.",
        "source": "Strength to Love (1963)"
    },
    {
        "id": 166,
        "author": "Lão Tử",
        "author_en": "Laozi",
        "author_title": "Nhà tư tưởng Trung Hoa cổ đại",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Nước là thứ mềm mại nhất trên đời, nhưng không có thứ gì cứng rắn có thể chống lại nó. Lấy nhu thắng cương, lấy nhược thắng cường.",
        "quote_en": "Nothing in the world is more soft and yielding than water, yet for attacking things that are firm and strong, nothing excels it.",
        "source": "Đạo Đức Kinh (Chương 78)"
    },
    {
        "id": 167,
        "author": "Albert Einstein",
        "author_en": "Albert Einstein",
        "author_title": "Nhà vật lý lý thuyết đoạt giải Nobel",
        "era": "Thế kỷ 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Thế giới này gặp nguy hiểm không phải bởi những kẻ làm điều ác, mà bởi những người đứng nhìn mà không làm gì cả.",
        "quote_en": "The world is a dangerous place to live; not because of the people who are evil, but because of the people who don't do anything about it.",
        "source": "Bút ký triết học Albert Einstein"
    },
    {
        "id": 168,
        "author": "Mạnh Tử",
        "author_en": "Mencius",
        "author_title": "Nhà triết học Nho gia (Á Thánh)",
        "era": "Thế kỷ thứ 4 TCN",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Phú quý bất năng dâm, bần tiện bất năng di, uy vũ bất năng khuất. Thử chi vị đại trượng phu (Giàu sang không buông thả, nghèo khó không đổi lòng, uy quyền bạo lực không khuất phục. Đó mới gọi là bậc đại trượng phu).",
        "quote_en": "To be above the power of riches and honors to make dissipated, of poverty and mean condition to make swerve from principle, and of power and force to make bend – these characteristics constitute the great man.",
        "source": "Mạnh Tử (Đằng Văn Công hạ)"
    },
    {
        "id": 169,
        "author": "Mahatma Gandhi",
        "author_en": "Mahatma Gandhi",
        "author_title": "Lãnh tụ vĩ đại người Ấn Độ",
        "era": "Thế kỷ 19 - 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Sự vĩ đại của một quốc gia và tiến bộ đạo đức của nó có thể được đánh giá qua cách quốc gia đó đối xử với những con vật và kẻ yếu thế.",
        "quote_en": "The greatness of a nation and its moral progress can be judged by the way its animals are treated.",
        "source": "Tuyển tập tư tưởng Gandhi"
    },
    {
        "id": 170,
        "author": "Seneca",
        "author_en": "Lucius Annaeus Seneca",
        "author_title": "Triết gia Khắc kỷ La Mã",
        "era": "Thế kỷ thứ 1",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Bất cứ nơi nào có một con người, ở đó luôn có cơ hội cho lòng nhân ái.",
        "quote_en": "Wherever there is a human being, there is an opportunity for a kindness.",
        "source": "Về đời sống hạnh phúc (De Vita Beata)"
    },
    {
        "id": 171,
        "author": "Immanuel Kant",
        "author_en": "Immanuel Kant",
        "author_title": "Triết gia người Đức thời Khai sáng",
        "era": "Thế kỷ 18",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Hai điều khiến tâm hồn tôi tràn ngập sự ngưỡng mộ và kính sợ ngày càng tăng: bầu trời đầy sao trên đầu tôi và quy luật đạo đức bên trong tôi.",
        "quote_en": "Two things fill the mind with ever new and increasing admiration and awe: the starry heavens above me and the moral law within me.",
        "source": "Phê phán lý tính thực hành (Critique of Practical Reason, 1788)"
    },
    {
        "id": 172,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà tư tưởng thời Xuân Thu",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Người quân tử yêu cầu ở chính mình, kẻ tiểu nhân yêu cầu ở người khác.",
        "quote_en": "What the superior man seeks is in himself; what the small man seeks is in others.",
        "source": "Luận Ngữ (Vệ Linh Công)"
    },
    {
        "id": 173,
        "author": "Nelson Mandela",
        "author_en": "Nelson Mandela",
        "author_title": "Tổng thống Nam Phi, giải Nobel Hòa bình",
        "era": "Thế kỷ 20 - 21",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Lòng căm hận giống như việc bạn uống thuốc độc rồi hy vọng kẻ thù của mình sẽ chết.",
        "quote_en": "Resentment is like drinking poison and then hoping it will kill your enemies.",
        "source": "Tự truyện Nelson Mandela"
    },
    {
        "id": 174,
        "author": "Voltaire",
        "author_en": "Voltaire",
        "author_title": "Đại văn hào, triết gia thời Khai sáng người Pháp",
        "era": "Thế kỷ 18",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Tôi có thể không đồng ý với những gì bạn nói, nhưng tôi sẽ bảo vệ đến chết quyền được nói điều đó của bạn.",
        "quote_en": "I disapprove of what you say, but I will defend to the death your right to say it.",
        "source": "Tác phẩm The Friends of Voltaire (Evelyn Beatrice Hall tóm lược)"
    },
    {
        "id": 175,
        "author": "Mark Twain",
        "author_en": "Mark Twain",
        "author_title": "Đại văn hào người Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Lòng tốt là thứ ngôn ngữ mà người khiếm thính có thể nghe thấy và người khiếm thị có thể nhìn thấy.",
        "quote_en": "Kindness is the language which the deaf can hear and the blind can see.",
        "source": "Châm ngôn Mark Twain"
    },
    {
        "id": 176,
        "author": "Nguyễn Du",
        "author_en": "Nguyen Du",
        "author_title": "Đại thi hào dân tộc Việt Nam, danh nhân văn hóa thế giới, tác giả Truyện Kiều",
        "era": "Thế kỷ 18 - 19",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Thiện căn ở tại lòng ta, Chữ tâm kia mới bằng ba chữ tài.",
        "quote_en": "The root of goodness resides within our heart; that single word 'Heart' outweighs talent threefold.",
        "source": "Đoạn Trường Tân Thanh (Truyện Kiều, câu 3251-3252)"
    },
    {
        "id": 177,
        "author": "Maya Angelou",
        "author_en": "Maya Angelou",
        "author_title": "Nhà thơ, nhà văn, nhà hoạt động dân quyền người Mỹ",
        "era": "Thế kỷ 20 - 21",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Tôi đã học được rằng mọi người sẽ quên những gì bạn nói, mọi người sẽ quên những gì bạn làm, nhưng mọi người sẽ không bao giờ quên cảm xúc mà bạn mang lại cho họ.",
        "quote_en": "I've learned that people will forget what you said, people will forget what you did, but people will never forget how you made them feel.",
        "source": "Phát biểu và bút ký Maya Angelou"
    },
    {
        "id": 178,
        "author": "Albert Camus",
        "author_en": "Albert Camus",
        "author_title": "Nhà văn, triết gia Pháp đoạt giải Nobel",
        "era": "Thế kỷ 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Đừng đi trước tôi, tôi có thể không theo kịp. Đừng đi sau tôi, tôi có thể không dẫn đường. Hãy đi bên cạnh tôi và làm bạn của tôi.",
        "quote_en": "Don't walk in front of me… I may not follow. Don't walk behind me… I may not lead. Walk beside me… just be my friend.",
        "source": "Tác phẩm triết học Albert Camus"
    },
    {
        "id": 179,
        "author": "Epictetus",
        "author_en": "Epictetus",
        "author_title": "Triết gia Khắc kỷ Hy Lạp cổ đại",
        "era": "Thế kỷ thứ 1 - 2",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Chúng ta có hai tai và một miệng để chúng ta có thể lắng nghe nhiều gấp đôi nói.",
        "quote_en": "We have two ears and one mouth so that we can listen twice as much as we speak.",
        "source": "Mảnh đoạn triết học Epictetus"
    },
    {
        "id": 180,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Chủ tịch nước Việt Nam Dân chủ Cộng hòa",
        "era": "Thế kỷ 20",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Non sông Việt Nam có trở nên tươi đẹp hay không, dân tộc Việt Nam có bước tới đài vinh quang để sánh vai với các cường quốc năm châu được hay không, chính là nhờ một phần lớn ở công học tập của các em.",
        "quote_en": "Whether the mountains and rivers of Vietnam become glorious, and whether the Vietnamese nation can step onto the stage of glory to stand shoulder to shoulder with the powers of the five continents, depends in great part on your study.",
        "source": "Thư gửi học sinh nhân ngày khai trường đầu tiên (1945)"
    },
    {
        "id": 181,
        "author": "Socrates",
        "author_en": "Socrates",
        "author_title": "Triết gia Hy Lạp cổ đại",
        "era": "Thế kỷ thứ 5 TCN",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Hãy tử tế với mọi người, bởi vì bất kỳ ai bạn gặp cũng đang chiến đấu trong một cuộc chiến vô cùng khó khăn.",
        "quote_en": "Be kind, for everyone you meet is fighting a hard battle.",
        "source": "Châm ngôn triết học Cổ điển"
    },
    {
        "id": 182,
        "author": "Desmond Tutu",
        "author_en": "Desmond Tutu",
        "author_title": "Tổng giám mục Nam Phi, nhà hoạt động nhân quyền giải Nobel Hòa bình",
        "era": "Thế kỷ 20 - 21",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Hãy làm chút việc tốt nhỏ bé ở nơi bạn đang sống; chính những mảnh việc tốt nhỏ bé gom góp lại sẽ làm tràn ngập thế giới.",
        "quote_en": "Do your little bit of good where you are; it's those little bits of good put together that overwhelm the world.",
        "source": "Thông điệp hòa bình Desmond Tutu"
    },
    {
        "id": 183,
        "author": "Khổng Tử",
        "author_en": "Confucius",
        "author_title": "Nhà tư tưởng thời Xuân Thu",
        "era": "Thế kỷ thứ 6 TCN",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Người quân tử hòa mà không đồng, kẻ tiểu nhân đồng mà không hòa.",
        "quote_en": "The gentleman agrees with others without following blindly; the small man follows blindly without agreeing in spirit.",
        "source": "Luận Ngữ (Tử Lộ)"
    },
    {
        "id": 184,
        "author": "Marcus Aurelius",
        "author_en": "Marcus Aurelius",
        "author_title": "Hoàng đế La Mã, triết gia Khắc kỷ",
        "era": "Thế kỷ thứ 2",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Cách trả thù tốt nhất là đừng giống như kẻ đã làm hại bạn.",
        "quote_en": "The best revenge is not to be like that.",
        "source": "Suy tưởng (Meditations, Quyển 6)"
    },
    {
        "id": 185,
        "author": "Thích Nhất Hạnh",
        "author_en": "Thich Nhat Hanh",
        "author_title": "Thiền sư Việt Nam",
        "era": "Thế kỷ 20 - 21",
        "category": "Đạo đức & Nhân cách",
        "quote_vi": "Thấu hiểu chính là tên gọi khác của tình thương yêu. Nếu bạn không thể thấu hiểu, bạn không thể thực sự yêu thương.",
        "quote_en": "Understanding is the other name of love. If you cannot understand, you cannot love.",
        "source": "Tác phẩm Giận (Anger, 2001)"
    },

    # =========================================================================
    # PHẦN 8: DŨNG CẢM, VƯỢT QUA NỖI SỢ & TỰ DO (COURAGE & FREEDOM) - 15 CÂU
    # =========================================================================
    {
        "id": 186,
        "author": "Nelson Mandela",
        "author_en": "Nelson Mandela",
        "author_title": "Tổng thống Nam Phi, giải Nobel Hòa bình",
        "era": "Thế kỷ 20 - 21",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Tôi học được rằng lòng dũng cảm không phải là sự vắng bóng của nỗi sợ hãi, mà là sự chiến thắng nỗi sợ hãi đó. Người dũng cảm không phải là người không biết sợ, mà là người dám vượt lên nỗi sợ hãi.",
        "quote_en": "I learned that courage was not the absence of fear, but the triumph over it. The brave man is not he who does not feel afraid, but he who conquers that fear.",
        "source": "Tự truyện Long Walk to Freedom (1994)"
    },
    {
        "id": 187,
        "author": "Chủ tịch Hồ Chí Minh",
        "author_en": "Ho Chi Minh",
        "author_title": "Chủ tịch nước Việt Nam Dân chủ Cộng hòa",
        "era": "Thế kỷ 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Không có gì quý hơn độc lập, tự do!",
        "quote_en": "Nothing is more precious than independence and freedom!",
        "source": "Lời kêu gọi đồng bào và chiến sĩ cả nước (17/7/1966)"
    },
    {
        "id": 188,
        "author": "Franklin D. Roosevelt",
        "author_en": "Franklin D. Roosevelt",
        "author_title": "Tổng thống thứ 32 của Hoa Kỳ",
        "era": "Thế kỷ 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Điều duy nhất chúng ta phải sợ hãi chính là bản thân nỗi sợ hãi.",
        "quote_en": "The only thing we have to fear is fear itself.",
        "source": "Diễn văn nhậm chức Tổng thống đầu tiên (1933)"
    },
    {
        "id": 189,
        "author": "Mark Twain",
        "author_en": "Mark Twain",
        "author_title": "Đại văn hào người Mỹ",
        "era": "Thế kỷ 19 - 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Hai mươi năm sau kể từ bây giờ, bạn sẽ thất vọng vì những điều bạn đã không làm nhiều hơn là những điều bạn đã làm. Vì vậy hãy tháo dây neo, căng buồm ra khơi rời khỏi bến đỗ an toàn. Hãy khám phá, hãy ước mơ, hãy kiếm tìm.",
        "quote_en": "Twenty years from now you will be more disappointed by the things that you didn't do than by the ones you did do. So throw off the bowlines. Sail away from the safe harbor. Catch the trade winds in your sails. Explore. Dream. Discover.",
        "source": "Tập văn Jackson Brown trích dẫn Mark Twain"
    },
    {
        "id": 190,
        "author": "Winston Churchill",
        "author_en": "Winston Churchill",
        "author_title": "Thủ tướng Anh thời Thế chiến II",
        "era": "Thế kỷ 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Lòng can đảm là đức tính quan trọng nhất của con người, bởi vì nó là đức tính bảo đảm cho tất cả những đức tính còn lại.",
        "quote_en": "Courage is the first of human qualities because it is the quality which guarantees all others.",
        "source": "Diễn văn tại Hạ viện Anh"
    },
    {
        "id": 191,
        "author": "Bà Trưng Trắc",
        "author_en": "Trung Trac (Hai Ba Trung)",
        "author_title": "Nữ thủ lĩnh đầu tiên khởi nghĩa giành độc lập cho dân tộc Việt Nam",
        "era": "Năm 40",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Một xin rửa sạch nước thù, Hai xin đem lại nghiệp xưa họ Hùng, Ba kẻo oan ức lòng chồng, Bốn xin vẹn vẹn sở công lênh này.",
        "quote_en": "First, to wash away the nation's shame; second, to restore the ancient heritage of the Hung kings; third, to avenge my husband's unjust death; fourth, to fulfill this glorious mission.",
        "source": "Lời thề Hát Môn (Đại Nam Quốc Sử Diễn Ca)"
    },
    {
        "id": 192,
        "author": "Malala Yousafzai",
        "author_en": "Malala Yousafzai",
        "author_title": "Người đoạt giải Nobel Hòa bình trẻ nhất lịch sử (17 tuổi)",
        "era": "Thế kỷ 21",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Một đứa trẻ, một giáo viên, một cuốn sách và một cây bút có thể thay đổi cả thế giới.",
        "quote_en": "One child, one teacher, one book, one pen can change the world.",
        "source": "Bài phát biểu tại Đại hội đồng Liên Hợp Quốc (2013)"
    },
    {
        "id": 193,
        "author": "Rosa Parks",
        "author_en": "Rosa Parks",
        "author_title": "Biểu tượng phong trào dân quyền người Mỹ gốc Phi",
        "era": "Thế kỷ 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Tôi đã học được qua năm tháng rằng khi một người có quyết tâm cao độ, điều đó sẽ làm tan biến nỗi sợ hãi; biết được điều gì phải làm sẽ loại bỏ mọi sự sợ hãi.",
        "quote_en": "I have learned over the years that when one's mind is made up, this diminishes fear; knowing what must be done does away with fear.",
        "source": "Hồi ký Rosa Parks"
    },
    {
        "id": 194,
        "author": "Bà Triệu (Triệu Thị Trinh)",
        "author_en": "Lady Trieu",
        "author_title": "Nữ anh hùng dân tộc Việt Nam chống quân Đông Ngô",
        "era": "Năm 248",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Tôi muốn cưỡi cơn gió mạnh, đạp luồng sóng dữ, chém cá kình ở biển Đông, lấy lại giang sơn, dựng nền độc lập, cởi ách nô lệ, chứ không chịu khom lưng làm tì thiếp cho người!",
        "quote_en": "I want to ride the strong winds, tread the fierce waves, slay the whales in the Eastern Sea, reclaim our land, build independence, and shake off the yoke of slavery, rather than bend my back as a concubine!",
        "source": "Đại Việt Sử Ký Toàn Thư"
    },
    {
        "id": 195,
        "author": "Plato",
        "author_en": "Plato",
        "author_title": "Triết gia Hy Lạp cổ đại",
        "era": "Thế kỷ thứ 5 - 4 TCN",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Lòng dũng cảm là biết điều gì không cần phải sợ.",
        "quote_en": "Courage is knowing what not to fear.",
        "source": "Các đối thoại Socrates của Plato"
    },
    {
        "id": 196,
        "author": "Neil Armstrong",
        "author_en": "Neil Armstrong",
        "author_title": "Phi hành gia người Mỹ, con người đầu tiên đặt chân lên Mặt Trăng",
        "era": "Thế kỷ 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Đây là một bước đi nhỏ của một con người, nhưng là một bước tiến vĩ đại của toàn thể nhân loại.",
        "quote_en": "That's one small step for man, one giant leap for mankind.",
        "source": "Tuyên bố khi bước xuống bề mặt Mặt Trăng (Apollo 11, 20/7/1969)"
    },
    {
        "id": 197,
        "author": "Amelia Earhart",
        "author_en": "Amelia Earhart",
        "author_title": "Nữ phi công tiên phong đầu tiên bay một mình qua Đại Tây Dương",
        "era": "Thế kỷ 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Điều khó khăn nhất chính là quyết định hành động; phần còn lại chỉ là sự ngoan cường và bền bỉ mà thôi.",
        "quote_en": "The most difficult thing is the decision to act; the rest is merely tenacity.",
        "source": "Hồi ký phi công Amelia Earhart"
    },
    {
        "id": 198,
        "author": "Christopher Columbus",
        "author_en": "Christopher Columbus",
        "author_title": "Nhà thám hiểm người Ý dẫn đầu các chuyến hải hành khám phá châu Mỹ",
        "era": "Thế kỷ 15 - 16",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Bạn không bao giờ có thể vượt qua đại dương trừ khi bạn có đủ dũng khí để đánh mất dấu vết của bờ biển.",
        "quote_en": "You can never cross the ocean until you have the courage to lose sight of the shore.",
        "source": "Nhật ký hàng hải Columbus"
    },
    {
        "id": 199,
        "author": "George Eliot",
        "author_en": "George Eliot (Mary Ann Evans)",
        "author_title": "Đại văn hào người Anh thế kỷ 19",
        "era": "Thế kỷ 19",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Không bao giờ là quá muộn để trở thành con người mà bạn có thể đã từng trở thành.",
        "quote_en": "It is never too late to be what you might have been.",
        "source": "Tác phẩm và tư tưởng của George Eliot"
    },
    {
        "id": 200,
        "author": "Albert Einstein",
        "author_en": "Albert Einstein",
        "author_title": "Nhà vật lý lý thuyết vĩ đại nhất thế kỷ 20",
        "era": "Thế kỷ 20",
        "category": "Lòng dũng cảm & Thử thách",
        "quote_vi": "Chỉ có hai cách để bạn sống cuộc đời mình: Một là coi như không có phép màu nào xảy ra; Hai là coi như mọi thứ diễn ra đều là một phép màu kỳ diệu.",
        "quote_en": "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.",
        "source": "Tư tưởng triết học Albert Einstein"
    }
]

def main():
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "OUTPUT"))
    os.makedirs(output_dir, exist_ok=True)
    target_path = os.path.join(output_dir, "cau_noi_vi_nhan.json")

    # Kiểm tra tính toàn vẹn của dữ liệu
    assert len(QUOTES) == 200, f"Lỗi: Số lượng câu nói là {len(QUOTES)}, không đúng 200 câu!"

    ids = set()
    categories = {}
    for idx, q in enumerate(QUOTES, 1):
        assert q["id"] == idx, f"ID không khớp ở vị trí {idx}: {q['id']}"
        assert q["id"] not in ids, f"Trùng ID: {q['id']}"
        ids.add(q["id"])
        
        # Kiểm tra các trường bắt buộc
        for field in ["author", "author_en", "author_title", "era", "category", "quote_vi", "quote_en", "source"]:
            assert field in q and q[field].strip(), f"Trường {field} bị trống tại ID {q['id']}"

        cat = q["category"]
        categories[cat] = categories.get(cat, 0) + 1

    # Tạo đối tượng metadata đóng gói hoàn chỉnh
    dataset = {
        "title": "Bộ sưu tập 200 câu nói kinh điển của các vĩ nhân trên thế giới",
        "total_quotes": len(QUOTES),
        "language": ["Tiếng Việt", "English"],
        "created_at": "2026-10-30",
        "version": "1.0",
        "categories_summary": categories,
        "quotes": QUOTES
    }

    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    print(f"Đã xuất thành công {len(QUOTES)} câu nói ra tệp: {target_path}")
    print(f"Kích thước tệp: {os.path.getsize(target_path)} bytes")
    print("Phân bố danh mục:")
    for cat, count in categories.items():
        print(f" - {cat}: {count} câu")

if __name__ == "__main__":
    main()
