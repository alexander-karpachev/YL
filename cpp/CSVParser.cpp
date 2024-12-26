#include <iostream>
#include <fstream>
#include <ostream>
#include <istream>
#include <tuple>
#include <string>
#include <type_traits>
#include <iterator>
#include <sstream>
#include <list>
#include <vector>

// остановка рекурсии
template <std::size_t I = 0, typename... Args, typename Ch, typename Tr>
typename std::enable_if< ( I == sizeof...(Args) ),void>::type 
printTuple(std::basic_ostream<Ch, Tr>& os, std::tuple<Args...> t)
{
    return;
}

// тело рекурсии
template <size_t I = 0, typename... Args, typename Ch, typename Tr>
typename std::enable_if<( I < sizeof...(Args) ),void>::type 
printTuple(std::basic_ostream<Ch, Tr>& os, std::tuple<Args...> t)
{
    if (I > 0) os << ", ";
    os << std::get<I>(t);
    printTuple<I + 1>(os, t);
}

template <typename... Args, typename Ch, typename Tr>
std::ostream& operator <<(std::basic_ostream<Ch, Tr>& os, std::tuple<Args...> const& t) {
    printTuple(os, t); 
    return os;
}

//=================================================================================================
// конвертация строки в базовый тип
template <typename T>
T convert(std::string const& x)
{
    if constexpr (std::is_same<T, int>::value)              return std::stoi(x.c_str());
    if constexpr (std::is_same<T, float>::value)            return std::stof(x.c_str());
    if constexpr (std::is_same<T, double>::value)           return std::stof(x.c_str());
    if constexpr (std::is_same<T, std::string>::value)      return x;
}
// конвертация колонок
template<class... Ts, size_t... Idxs>
std::tuple<Ts...>
//parse(std::vector<std::string> const& values, std::index_sequence<Idxs...>) {
parse(std::vector<std::string> const& values, std::index_sequence<Idxs...>) {
    return {convert<Ts>(values[Idxs])...};
}
// конвертация списка строк в tuple
template<class... Ts>
std::tuple<Ts...> vector2tuple(std::vector<std::string> const& values) {
    return parse<Ts...>(values, std::make_index_sequence<sizeof...(Ts)>{});
}



// параметры парсера по-умолчанию
#if !defined(CSVPARSER_DELIM)
#define CSVPARSER_DELIM ','
#endif

#if !defined(CSVPARSER_EOL)
#define CSVPARSER_EOL '\n'
#endif

#if !defined(CSVPARSER_ESCAPE)
#define CSVPARSER_ESCAPE '"'
#endif

template <typename... Args>
class CSVParser
{
    private:
        using val = std::tuple<Args...>;
        std::ifstream& file_;
        val current_; // текущий сет
        
        int line_ = 1;    // номер текущей строки
        int column_ = 0;  // номер текущей колонки
        bool err_ = false; // флаг ошибки парсинга

        int N; // кол-во строк, которые пропускает с начала файла
        char delim = CSVPARSER_DELIM; // разделитель колонок
        char endl = CSVPARSER_EOL;  // разделитель строк
        char escap = CSVPARSER_ESCAPE;   // экранирование
    public:
        class iterator
        {
            CSVParser* x_;
        public:
            using value_type = val;
            using reference = const val&;
            using pointer = const val*;
            using iterator_category = std::input_iterator_tag;

            iterator(CSVParser* x=nullptr): x_ {x} { }
            reference operator*() const { return x_->current_; }
            iterator& operator++() { increment(); return *this; }
            iterator operator++(int) { increment(); return *this; }
            bool operator==(iterator rhs) const { return x_ == rhs.x_; }
            bool operator!=(iterator rhs) const { return !(rhs==*this); }
        protected:
            void increment()
            {
                if (!x_->valid())
                {
                    x_ = nullptr;
                    return;
                }
                x_->next();
            }
        };    
        iterator begin() { return iterator{this}; }
        iterator end() { return iterator{}; }

        // Конструктор по заданию
        CSVParser(std::ifstream& f, int const skip_lines = 0) : file_(f), N(skip_lines) 
        {   
            for(int i = 0; i < N; ++i ) skip();
            next(); 
        } // итератор сразу дергает операцию *, поэтому для него сразу парсим первую строку 
        // Конфигуратор. Устанавливает флаг cust_flag в зависимости от заданных настроек
        void setDelimeter(char const d = CSVPARSER_DELIM) 
        {
            if ( d == '\0' ) return;
            this->delim = d;
        }
        void setEOL(char const eol = CSVPARSER_EOL) 
        { 
            if ( eol == '\0' ) return;
            this->endl = eol; 
        }
        void setESCAPE(char const esc = CSVPARSER_ESCAPE) 
        { 
            if ( esc == '\0' ) return;
            this->escap = esc; 
        }
        bool valid() const 
        {
            return !file_.eof() && !err_;
        }
        void skip() // пропускает 1 строку
        {
            char c;
            while(file_.get(c))
            {
               if ( c == endl ) break;
            }
            ++line_;
        }
        void next() 
        {
            using tmp_store = std::vector<std::string>;
            bool escaped = false; //флаг отмечает был ли встречен символ экранирования
            char c;
            std::string ss;
            int i = 0;
            int max_i = std::tuple_size<val>{};
            tmp_store tmp;
            while(file_.get(c))
            {
                if ( c == escap ) { escaped = !escaped; continue; }
                if ( escaped    ) { ss += c;            continue; }
                if ( c == delim || c == endl ) 
                { 
                    // TODO: Может возникнуть исключение преобразования
                    // сохраняем полученную колонку
                    tmp.push_back(std::move(ss));
                    //p1 = convert<T1>(ss); 
                    ++i;
                    ss.clear();
                    if (c == endl || i == max_i) break; // встретив конец строки или собрав все колонки - выходим
                    continue; 
                }
                ss += c;
            }
            if ( escaped ) { /* TODO: кинуть исключение - не закрыт символ экранирования до конца файла*/ }
            if ( line_ > N ) // здесь проверка на пропуск строк 
            {
                if ( i < max_i ) tmp.push_back(std::move(ss));
                
                try 
                {
                    auto t = vector2tuple<Args...>(tmp);
                    current_ = std::move(t);
                }
                catch(const std::exception &exc)
                {
                    std::cout << "Parsing error. Line: "<< line_ << std::endl;
                    err_= true;
                }
            }
            //std::cout << " >>> Line: "<< line_ << std::endl;
            ++line_;
        }
};

int main() {

    std::ifstream file("test002.csv");
    CSVParser<int, std::string, double> parser {file, 0};
    //parser.setEOL(';');
    for (std::tuple<int, std::string, double> rs : parser)
    {
       std::cout << rs << std::endl;
    }

    return 0;
} 